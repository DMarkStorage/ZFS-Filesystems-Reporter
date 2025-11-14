"""
ZFS Filesystems Reporter

This script connects to a ZFS appliance, retrieves filesystem information
via its REST API, and writes selected fields to CSV and JSON files.

It expects credentials to be stored in a Vault path, which is read to
construct the required authentication headers.
"""

import requests
import pandas as pd
from docopt import docopt
from tabulate import tabulate

sys.path.append('/home/storagetools')

from mods.common.vault.ver2.vault import Vault
import traceback

requests.packages.urllib3.disable_warnings()


__version__ = '1.0'
__revision__ = '20190626'
__deprecated__ = False



global_data_store = {}

def get_headers():
    """
    Build and return HTTP request headers for the ZFS API.

    Secrets (username and password) are retrieved from Vault using a fixed path.
    If the secret fetch fails, an exception is raised.

    Returns:
        dict: Headers including Content-Type, X-Auth-User, and X-Auth-Key.

    Raises:
        Exception: If secrets cannot be retrieved from the Vault path.
    """
    vault_path = 'it-storage/KVv1/oracle/ZFS/zapi_ro_user'
    secrets = Vault(vault_path).get_secret()
    if secrets['Error']:
        error_msg = f'Failed to retrieve secrets from vault path: {vault_path}'
        raise Exception(error_msg)
    request_headers = {
        'Content-Type': 'application/json',
        'X-Auth-User': secrets['Data']['username'],
        'X-Auth-Key': secrets['Data']['password']
    }
    return request_headers


def get_args():
    """
    Parse command-line arguments using docopt.

    Expected usage:
        Filesystems_Reporter.py -s <STORAGE> -fl <FILENAME> [-v <NUM> | --view <NUM>]
        Filesystems_Reporter.py --version
        Filesystems_Reporter.py -h | --help

    Returns:
        dict: Parsed arguments as returned by docopt.
              Keys include '<STORAGE>' and '<FILENAME>'.
    """
    usage = """
    Usage:
        Filesystems_Reporter.py -s <STORAGE> -fl <FILENAME> [-v <NUM> | --view <NUM>]
        Filesystems_Reporter.py --version
        Filesystems_Reporter.py -h | --help

    Options:
        -h --help            Show this message and exit
        -s <STORAGE>         ZFS appliance/storage name
        -fl <FILENAME>       Base filename (without extension) for output files
        -v <NUM>             View the first NUM rows in the CLI
        --view <NUM>         Same as -v
    """

    parsed_args = docopt(usage)
    return parsed_args


def get_projects(storage):
    """
    Query the ZFS appliance for filesystem information and forward the
    structured rows to the writer.

    Args:
        storage (str): Hostname or IP of the ZFS appliance.
    """
    request_headers = get_headers()
    base_url = f'https://{storage}:215'
    filesystems_url = f'{base_url}/api/storage/v1/filesystems'
    
    # Fetch data from API
    response = requests.get(url=filesystems_url, verify=False, headers=request_headers)
    response.raise_for_status()  # Raise exception for bad status codes
    
    filesystems = response.json().get('filesystems', [])
    
    # Extract relevant fields from each filesystem
    rows = []
    for fs in filesystems:
        row = [
            fs.get('name'),
            fs.get('pool'),
            fs.get('sharesmb'),
            fs.get('sharesmb_name', ''),  # Default to empty string if missing
            fs.get('sharenfs'),
            fs.get('shareftp'),
            fs.get('space_data'),
            fs.get('space_total')
        ]
        rows.append(row)
    
    return rows 


def write_data(rows, filename):
    """
    Convert collected filesystem rows into a pandas DataFrame and write
    both CSV and JSON files.

    Args:
        rows (list[list]): Each inner list is:
            [name, pool, sharesmb, sharesmb_name, sharenfs, shareftp, space_data, space_total]
        filename (str): Base filename (without extension) for output files.
    """
    try:
        # rows already contain scalar values per column
        # Directly create DataFrame from rows
        df = pd.DataFrame(
            rows,
            columns=['Name', 'Pool', 'ShareSMB', 'Sharesmb Name', 'Sharenfs',
                     'Shareftp', 'Space data', 'space_total']
        )
        df.to_csv(filename + '.csv', index=False)
        df.to_json(filename + '.json', indent=4, orient='records')
        print('Csv and json file Created')
    except Exception as e:
        print(e)

def view_rows(rows, count):
    """
    Print the first `count` rows in a pretty CLI table.

    Args:
        rows (list[list]): Each row shape:
            [Name, Pool, ShareSMB, Sharesmb Name, Sharenfs, Shareftp, Space data, space_total]
        count (int): Number of rows to display from the top.

    Behavior:
        - Uses 'fancy_grid' via tabulate when available.
        - Falls back to pandas' plain text rendering otherwise.
    """
    columns = ['Name', 'Pool', 'ShareSMB', 'Sharesmb Name',
               'Sharenfs', 'Shareftp', 'Space data', 'space_total']
    df = pd.DataFrame(rows, columns=columns)

    total_rows = len(df)
    try:
        count = max(0, int(count))
    except Exception:
        count = 5  # sensible default if parsing fails

    df_show = df.head(count)
    print(f"\n=== Filesystem Report (showing first {len(df_show)} of {total_rows} rows) ===")

    if _HAS_TABULATE:
        # Adjust maxcolwidths to your taste; order matches `columns` above
        print(_tabulate(
            df_show,
            headers='keys',
            tablefmt='fancy_grid',
            numalign='center',
            stralign='center',
            showindex=False,
            maxcolwidths=[20, 15, 22, 22, 22, 15, 14, 14]
        ))
    else:
        # Fallback if tabulate isn't installed
        print(df_show.to_string(index=False))

def main(cli_args):
    """
    Entry point that extracts CLI arguments and triggers data retrieval.

    Args:
        cli_args (dict): Parsed docopt arguments containing '<STORAGE>' and '<FILENAME>'.
    """
    storage = cli_args['<STORAGE>']
    filename = cli_args['<FILENAME>']
    
    print(f"Fetching data from {storage}...")
    rows = get_projects(storage)

    if not rows:
        print("No data retrieved from storage")
        return
    
    print(f"Retrieved {len(rows)} filesystems")

    # Support either -v <NUM> or --view <NUM>
    view_arg = cli_args.get('-v') or cli_args.get('--view')
    if view_arg is not None:
        try:
            requested = int(view_arg)
        except ValueError:
            print(f"[view] Invalid number: {view_arg}. Showing 3 rows instead.")
            requested = 3

        if requested <= 0:
            print(f"[view] Non-positive number: {requested}. Showing 3 rows instead.")
            requested = 3

        if requested > len(rows):
            print(f"[view] Requested {requested} rows, but only {len(rows)} available. Showing {len(rows)} rows instead.")
            display = len(rows)
        else:
            display = requested

        view_rows(rows, display)

    # Write data to files
    write_data(rows, filename)


if __name__ == '__main__':
    try:
        CLI_ARGS = get_args()
        main(CLI_ARGS)
    except KeyboardInterrupt:
        print('\nReceived Ctrl^C. Exiting....')
    except Exception:
        exception_traceback = traceback.format_exc()
        print(exception_traceback)

