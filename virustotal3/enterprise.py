""" VirusTotal API v3 Enterprise

Module to interact with the Enterprise part of the API.
"""
import os
import json
import requests


def _raise_exception(response):
    """Raise Exception

    Function to raise an exception using the error messages returned by the API.

    Parameters:
        response (dict): Reponse with the error returned by the API.
    """
    # https://developers.virustotal.com/v3.0/reference#errors
    raise Exception(response.text)


def search(api_key, query, order=None, limit=None, cursor=None,
           descriptors_only=None, proxies=None):
    """Search for files

    Search for files and return the file details.

    Parameters:
        api_key (str): VirusTotal API key
        query (str): Search query
        order (str, optional): Sort order. Can be one of the following:
                     size, positives, last_submission_date, first_submission_date,
                     times_submitted. Can be followed by a + or -.
                     Default is 'last_submission_date-'
        limit (int, optional): Maximum number of results to retrieve
        cursor (str, optional): Continuation cursor
        descriptors_only (bool, optional): Return file descriptor only instead of all details
        proxies (dict, optional): Dictionary with proxies

    Returns:
        A dict with the results from the search.
    """
    if api_key is None:
        raise Exception("You must provide a valid API key")

    try:
        params = {'query': query, 'order': order, 'limit': limit,
                  'cursor': cursor, 'descriptors_only': descriptors_only}
        response = requests.get('https://www.virustotal.com/api/v3/intelligence/search',
                                params=params,
                                headers={'x-apikey': api_key,
                                         'Accept': 'application/json'},
                                proxies=proxies)

        if response.status_code != 200:
            _raise_exception(response)

        json.dumps(response.json(), indent=4, sort_keys=True)

    except requests.exceptions.RequestException as error:
        print(error)
        exit(1)


def file_feed(api_key, time):
    """Get a file feed batch

    Get a file feed batch for a given date, by the minute. From the official
    documentation:
    "Time 201912010802 will return the batch corresponding to December 1st, 2019 08:02 UTC.
    You can download batches up to 7 days old, and the most recent batch has always a 5 minutes
    lag with respect with to the current time."

    Parameters:
        time (str): DYYYYMMDDhhmm
    """
    if api_key is None:
        raise Exception("You must provide a valid API key")

    try:
        response = requests.get('https://www.virustotal.com/api/v3/feeds/files/{}'.format(time),
                                headers={'x-apikey': api_key,
                                         'Accept': 'application/json'})

        if response.status_code != 200:
            _raise_exception(response)

        json.dumps(response.json(), indent=4, sort_keys=True)
    except requests.exceptions.RequestException as error:
        print(error)
        exit(1)


class Livehunt:
    """VT Enterprise Livehunt Endpoints

    Livehunt endpoints allowing to manage YARA rules and notifications.

    Attributes:
        api_key (str): VirusTotal API key
        proxies (dict, optional): Dictionary with proxies
    """

    def __init__(self, api_key=None, proxies=None):
        """
        Constructor for the Livehunt class.

        Parameters:
            api_key (str): VirusTotal API key
            proxies (dict, optional): Dictionary with proxies
        """
        self.api_key = api_key
        self.base_url = 'https://www.virustotal.com/api/v3/intelligence'
        self.headers = {'x-apikey': self.api_key,
                        'Accept': 'application/json'}
        self.proxies = proxies

        if api_key is None:
            raise Exception("You must provide a valid API key")

    def get_rulesets(self, ruleset_id=None, limit=None, fltr=None, order=None, cursor=None):
        """Retrieve one or multiple rulesets

        Retrieve a single ruleset for a given ID or all rulesets at once.

        Parameters:
            ruleset_id (str, optional): Ruleset ID required to return a single specific ruleset
            limit (int, optional): Maximum number of rulesets to retrieve
            fltr (str, optional): Return the rulesets matching the given criteria only
            order (str, optional): Sort order
            cursor (str, optional): Continuation cursor

        Returns:
            A dict with one or multiple rulesets.
        """
        try:
            if ruleset_id:
                params = {'id': ruleset_id}
                response = requests.get(self.base_url + '/hunting_rulesets/{}'.format(ruleset_id),
                                        headers=self.headers,
                                        params=params,
                                        proxies=self.proxies)
            else:
                params = {'limit': limit, 'fltr': fltr, 'order': order, 'cursor': cursor}
                response = requests.get(self.base_url + '/hunting_rulesets',
                                        headers=self.headers,
                                        params=params,
                                        proxies=self.proxies)
            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def create_rulset(self, data):
        """ Create a Livehunt ruleset

        Parameters:
            data (dict): Rule to create. See example below.

        Returns:
            A dict with the created rule.
        """
        try:
            response = requests.post(self.base_url + '/hunting_rulesets',
                                     data=json.dumps(data),
                                     headers=self.headers,
                                     proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def update_ruleset(self, ruleset_id, data):
        """ Update existing ruleset

        Update an existing ruleset for a given ID

        Parameters:
            ruleset_id (str): Ruleset ID
            data (dict): Ruleset to update as dictionary. The package will take care of creating the JSON object.
                         See example below.

        Returns:
            A dict with the updated rule.
        """
        try:
            response = requests.patch(self.base_url + '/hunting_rulesets/{}'.format(ruleset_id),
                                      data=json.dumps(data),
                                      headers=self.headers,
                                      proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def delete_ruleset(self, ruleset_id):
        """ Delete ruleset

        Delete ruleset for a given ID

        Parameters:
            ruleset_id (str): Ruleset ID

        Returns:
            None
        """
        try:
            response = requests.delete(self.base_url + '/hunting_rulesets/{}'.format(ruleset_id),
                                       headers=self.headers,
                                       proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return None

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def get_notifications(self, notification_id=None, limit=None, fltr=None, cursor=None):
        """Retrieve one or multiple notifications

        Retrieve a single notification for a given ID or all notifications at once.

        Parameters:
            notification_id (str, optional): Notification ID required to return a
                                             single specific ruleset.
            limit (int, optional): Maximum number of rulesets to retrieve
            fltr (str, optional): Return the rulesets matching the given criteria only
            cursor (str, optional): Continuation cursor

        Returns:
            A dict with one or multiple notifications in JSON format.
        """
        try:
            if notification_id:
                params = {'id': notification_id}
                response = requests.get(self.base_url + \
                                        '/hunting_notifications/{}'.format(notification_id),
                                        headers=self.headers,
                                        params=params)
            else:
                params = {'limit': limit, 'fltr': fltr, 'cursor': cursor}
                response = requests.get(self.base_url + '/hunting_notifications',
                                        headers=self.headers,
                                        proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def delete_notifications(self, tag):
        """ Delete notifications

        Delete notifications for a given tag

        Parameters:
            tag (str): Notification tag

        Returns:
            None
        """
        try:
            params = {'tag': tag}
            response = requests.delete(self.base_url + '/hunting_notifications',
                                       headers=self.headers,
                                       params=params,
                                       proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return None

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def delete_notification(self, notification_id):
        """Delete a single notification

        Delete a notification for a given notification ID

        Parameters:
            notification_id (str): Notification ID

        Returns:
            None
        """
        try:
            params = {'id': notification_id}
            response = requests.delete(self.base_url + '/hunting_notifications',
                                       headers=self.headers,
                                       params=params,
                                       proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return None

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def get_notification_files(self, limit=None, cursor=None):
        """Retrieve file objects for notifications

        Retrieve file details and context attributes from notifications.

        Parameters:
            limit (int, optional): Maximum number of rulesets to retrieve
            cursor (str, optional): Continuation cursor

        Returns:
            A dict with one or multiple notifications.
        """
        try:
            params = {'limit': limit, 'cursor': cursor}
            response = requests.get(self.base_url + '/hunting_notification_files',
                                    headers=self.headers,
                                    params=params,
                                    proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)


class Retrohunt:
    """VirusTotal Retrohunt class

    Run Retrohunting jobs.
    """

    def __init__(self, api_key=None, proxies=None):
        """
        Constructor for the Retrohunt class.

        Parameters:
            api_key (str): VirusTotal API key
            proxies (dict, optional): Dictionary with proxies
        """
        self.api_key = api_key
        self.base_url = 'https://www.virustotal.com/api/v3/intelligence'
        self.headers = {'x-apikey': self.api_key,
                        'Accept': 'application/json'}
        self.proxies = proxies

    def get_jobs(self, job_id=None, limit=None, fltr=None, cursor=None):
        """ Retrieve a Retrohunt job

        Retrieve an existing Retrohunt jobs. Returns all jobs if no ID is specified.

        Parameters:
            job_id (str, optional): Job ID
            limit (int, optional): Maximum number of jobs to retrieve
            fltr (str, optional): Filter matching specific jobs only
            cursor (str, optional): Continuation cursor

        Returns:
            A dict with one of multiple jobs.
        """
        try:
            if job_id:
                params = {'id': job_id}
                response = requests.get(self.base_url + '/Retrohunt_jobs/{}'.format(job_id),
                                        headers=self.headers,
                                        params=params,
                                        proxies=self.proxies)
            else:
                params = {'limit': limit, 'fltr': fltr, 'cursor': cursor}
                response = requests.get(self.base_url + '/Retrohunt_jobs',
                                        headers=self.headers,
                                        params=params,
                                        proxies=self.proxies)
            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def create_job(self, data):
        """ Create a Retrohunt job

        Create a new Retrohunt job

        Parameters:
            data (dict): Rule to create. See example below.

        Returns:
            A dict with the created rule.
        """
        try:
            response = requests.post(self.base_url + '/Retrohunt_jobs',
                                     data=json.dumps(data),
                                     headers=self.headers,
                                     proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def delete_job(self, job_id):
        """ Delete a job

        Delete a job for a given ID

        Parameters:
            job_id (str): Job ID

        Returns:
            None
        """
        try:
            response = requests.delete(self.base_url + '/Retrohunt_jobs/{}'.format(job_id),
                                       headers=self.headers,
                                       proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return None

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def abort_job(self, job_id):
        """ Abort a job

        Abort a job for a given ID

        Parameters:
            job_id (str): Job ID

        Returns:
            None
        """
        try:
            response = requests.post(self.base_url + '/Retrohunt_jobs/{}/abort'.format(job_id),
                                     headers=self.headers,
                                     proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return None

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def get_matching_files(self, job_id):
        """Get matching files

        Get matching files for a job ID

        Parameters:
            job_id (str): Job ID

        Returns:
            A dict with matching files
        """
        try:
            response = requests.get(self.base_url + \
                                    '/Retrohunt_jobs/{}/matching_files'.format(job_id),
                                    headers=self.headers,
                                    proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)


class Accounts:
    """VT Enterprise Users & Groups

    Manage and retrieve information on users and groups.

    This part of the API still is under development by VirusTotal.
    """

    def __init__(self, api_key=None, proxies=None):
        """
        Constructor for the Retrohunt class.

        Parameters:
            api_key (str): VirusTotal API key
            proxies (dict, optional): Dictionary with proxies
        """
        self.api_key = api_key
        self.base_url = 'https://www.virustotal.com/api/v3'
        self.headers = {'x-apikey': self.api_key,
                        'Accept': 'application/json'}
        self.proxies = proxies

    def info_user(self, user_id):
        """Retrieve information on a user

        Retrieve information on a user for a given ID

        Parameters:
            user_id (str): User ID

        Returns:
            A dict with the details on the user.
        """
        try:
            params = {'id': user_id}
            response = requests.get(self.base_url + '/users/{}'.format(user_id),
                                    headers=self.headers,
                                    params=params,
                                    proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def info_group(self, group_id):
        """Retrieve information on a group

        Retrieve information on a group for a given ID

        Parameters:
            group_id (str): User ID

        Returns:
            A dict with the details on the group.
        """
        try:
            response = requests.get(self.base_url + '/groups/{}'.format(group_id),
                                    headers=self.headers,
                                    proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def get_relationship(self, group_id, relationship, limit=None, cursor=None):
        """Retrieve objects related to a group

        Retrieve information on a user for a given group ID. Currently, the only relationship object supported by the
        VirusTotal v3 API is `graphs`.

        Parameters:
            group_id (str): User ID
            relationship (str): Relationship
            limit (str, optional): Limit of results to return
            cursor (str, optional): Continuation cursor

        Returns:
            A dict with the relationship object.
        """
        try:
            params = {'limit': limit, 'cursor': cursor}
            response = requests.get(self.base_url + \
                                    '/groups/{}/relationships/{}'.format(group_id, relationship),
                                    headers=self.headers,
                                    params=params,
                                    proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)


class ZipFiles:
    """Zipping files

    Zip and download an individual file or multiple files. Zip files are password protected.

    This part of the API still is under development by VirusTotal.
    """

    def __init__(self, api_key=None, proxies=None):
        """
        Constructor for the Retrohunt class.

        Parameters:
            api_key (str): VirusTotal API key
            proxies (dict, optional): Dictionary with proxies
        """
        self.api_key = api_key
        self.base_url = 'https://www.virustotal.com/api/v3/intelligence'
        self.headers = {'x-apikey': self.api_key,
                        'Accept': 'application/json'}
        self.proxies = proxies

    def create_zip(self, data):
        """Create a zip file

        Creates a password-protected ZIP file with files from VirusTotal.

        Parameters:
            data (str): Dictionary with a list of hashes to download. The format
                        should be the following:
                        {
                            "data": {
                                "password": "zipfilepassword",
                                "hashes":[
                                "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                                "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
                                "ed1707bf39a62b0efd40e76f55409ee99db0289dc5027d0a5e5337b4e7a61ccc"]
                            }
                        }
        Returns:
            A dict with the progression and status of the archive compression process, including its ID. Use the
            info_zip() function to check the status of a Zip file for a given ID.
        """
        try:
            response = requests.post(self.base_url + '/zip_files',
                                     headers=self.headers,
                                     data=json.dumps(data),
                                     proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def info_zip(self, zip_id):
        """Get the status of a Zip file

        Check the status of a Zip file for a given ID.

        Parameters:
            zip_id (str): ID of the zip file

        Returns:
            A dict with the status of the zip file creation. When the value of the 'status' key is set to 'finished',
            the file is ready for download. Other status are: 'starting', 'creating', 'timeout', 'error-starting',
            'error-creating'.
        """
        try:
            response = requests.get(self.base_url + '/zip_files/{}'.format(zip_id),
                                    headers=self.headers,
                                    proxies=self.proxies)

            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def get_url(self, zip_id):
        """Get the download URL of a Zip file

        Get the download URL of a Zip file for a given ID. Will raise an exception if the file is not yet ready to
        download. Should be called only after info_zip() returns a 'finished' status.

        Parameters:
            zip_id (str): ID of the zip file

        Returns:
            URL of the zip file to download
        """

        try:
            response = requests.get(self.base_url + '/zip_files/{}/download_url'.format(zip_id),
                                    headers=self.headers,
                                    proxies=self.proxies)
            if response.status_code != 200:
                _raise_exception(response)

            return json.dumps(response.json(), indent=4, sort_keys=True)

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)

    def get_zip(self, zip_id, output_dir):
        """Download a zip file

        Download a zip file for a given ID.

        Parameters:
            zip_id (str): ID of the zip file
            output_dir (str): Output directory where the file will be downloaded.
        """

        try:
            response = requests.get(self.base_url + '/zip_files/{}/download'.format(zip_id),
                                    headers=self.headers,
                                    proxies=self.proxies)
            if response.status_code != 200:
                _raise_exception(response)

            with open(output_dir + '{}.zip'.format(zip_id), 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

        except requests.exceptions.RequestException as error:
            print(error)
            exit(1)
        except os.error as error:
            print(error)
            exit(1)