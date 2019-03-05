# cgc-cli

cgc-cli is a tool for fetching data from CGC Seven Bridges API

## Setup

The script has been tested with Python 3.7
To setup, you should preferably use virtualenv and install the requirements from `requirements.txt` using

```
pip install -r requirements.txt
```

After installing, you should source the `setenv.sh` script to put the cgccli script on the path. To do that run
```
source <cgc-cli repo folder>/setenv.sh
```

Then you'll be able to run the commands as specified later.

## Usage

CLI Tool supports following operations:

 - List projects
 - List files in projects
 - Get specific file details
 - Update file details
 - Download file

Sample usage:
```
cgccli --token {token} projects list
cgccli --token {token} files list --project test/simons-genome-diversity-project-sgdp
cgccli --token {token} files stat --file {file_id}
cgccli --token {token} files update  --file {file_id} name=bla
cgccli --token {token} files update --file {file_id} metadata.sample_id=asdasf
cgccli --token {token} files download --file {file_id} --dest /tmp/foo.bar
```
Token can be retrieved by registering to ​ www.cancergenomicscloud.org/

On the website you can find some sample projects for testing out the application.
