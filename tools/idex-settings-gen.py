#!/usr/bin/env python3

# Copyright (c) 2020 Santiago Alessandri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import json
import logging
import requests
import secrets

from web3.auto import w3
from eth_account.messages import encode_defunct

BASE_URL = 'https://sc.idex.market'

def get_challenge(address):
    request_url = '{base_url}/wallet/{cold_wallet}/challenge'.format(
        base_url=BASE_URL,
        cold_wallet=address)

    response = requests.get(request_url)
    if response.status_code == 403:
        logging.info('Your cold wallet is not qualified for staking')
        return None
    elif response.status_code != 200:
        logging.error('Error retrieving the challenge. Status code: {}'.format(
            response.status_code))
        return None

    response_json = response.json()
    logging.debug('Received the following response: {}'.format(response_json))

    return response_json['message']

def validate_challenge(address, challenge, signed_challenge):
    try:
        signer_address = w3.eth.account.recover_message(encode_defunct(text=challenge),
                                                        signature=signed_challenge)
    except Exception as e:
        logging.error('Failure when recovering the signer: {}'.format(e))
        return False

    if signer_address.lower() != address.lower():
        logging.error('Signature validation failed!')
        return False
    return True

def submit_challenge(address, hot_wallet, signed_challenge):
    request_url = '{base_url}/wallet/{cold_wallet}/challenge'.format(
        base_url=BASE_URL,
        cold_wallet=address)

    data = {
        'hotWallet': hot_wallet.address,
        'signature': signed_challenge
    }

    response = requests.post(request_url, json=data)
    if response.status_code != 200:
        logging.error('Error retrieving the challenge. Status code: {}'.format(
            response.status_code))
        raise Exception()

def generate_settings_file(address, hot_wallet, output_file):
    token = secrets.token_hex(16)

    encrypted_wallet = hot_wallet.encrypt(token)

    settings_data = {
        'coldWallet': address,
        'token': token,
        'hotWallet': encrypted_wallet
    }

    logging.info('Generating settings file: {}'.format(output_file))

    with open(output_file, 'w') as f:
        json.dump(settings_data, f)

    logging.info('Settings file successfully generated')


def main(address, output_file):
    logging.info('Validating staking address and retrieving challenge')
    challenge = get_challenge(address)
    if challenge is None:
        return
    logging.debug('Challenge received: {}'.format(challenge))

    print('Please sign the following message (without quotes): "{}"'.format(challenge))
    signed_challenge = input('Enter the "sig" field value: ')

    logging.info('Validating challenge signature')
    if not validate_challenge(address, challenge, signed_challenge):
        return

    logging.info('Signature validated, submitting challenge')
    hot_wallet = w3.eth.account.create(secrets.token_hex(64))

    try:
        submit_challenge(address, hot_wallet, signed_challenge)
    except:
        return

    generate_settings_file(address, hot_wallet, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate settings file for IDEX staking node.')
    parser.add_argument('address', help='Address holding the IDEX tokens to stake')
    parser.add_argument('--output-file',
                         default='settings.json',
                         help='Destination file for the settings')

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    main(**vars(args))
