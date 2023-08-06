# STOCKS Python Client

This repo contains a (new) client module as interface to the STOCKS API. 
A CLI serves as ready-to-use tool well as example for further implementations.

## Development

```bash
# create a virtualenv/conda env 
conda create -n stocks-client python=3.10 && conda activate stocks-client

git clone https://git.embl.de/grp-gbcs/stocks-cli.git
cd stocks-cli
pip install -e .

# Display global help i.e. list modules
stocks-cli --help
# Display module help i.e. list modules commands
stocks-cli <module_name> --help 
# Display command help 
stocks-cli <module_name> <command_name> --help
```

## Configure
To use the CLI, you must first setup a user configuration file containing important connection information; this is by 
default stored in your home (`/my/home/.stocks/stocksapi.yml`).

For setup the STOCKS server to connect to, we use the `config` sub-module.  

Note for developers: you can set more than one server, and switch between those as need 

```bash
# Calling config setup will prompt you with defaults offered
stocks-cli config setup
# Alternatively one can provide values in the command line, your pwd will be prompted
stocks-cli config setup --stocks_url https://stocks.embl.de --stocks_user <username> --unix_group <group>

# You can check the content of your config with 
stocks-cli config show
# Or reset (wipe it altogether)
stocks-cli config clean
# Or switch to another configuration i.e. a locally running server or a test server (useful for developpers)
stocks-cli config switch --stocks-api-url http://127.0.0.1:8000/

```

## Global properties
Other configuration files are available to globally configure properties common to a STOCKS server 
- `cli/stockscli.ini` (email, institution name...)
- `cli/log_config.ini` (loggers)

## Using `jq`

`jq` can be used to format and parse the returned json:

### Fetch a list of datafile locations for a study

and format to a table for further processing

```bash
python stocks.py list datafilecopies study_uuid | jq -r '.results[]|[.shortname, .uri, .readtype] | @tsv'
```

### Create symbolic links to files stored in STOCKS

A similar approach as above can be used to easily make symbolic links to the files in the current directory
The last xargs will prompt for every symbolic link that is going to be made due to the `-p`.
```bash
python stocks.py list datafilecopies study_uuid | jq -r '.results[]|[.uri, .shortname] | @tsv' | xargs -p -n 2 ln -s
```

### Fetch all datafile copies belonging to a flowcell

and list them as a table, including the datafilecopy checksum and the status.

```bash
stocks list assay --query_param "flowcell=000000000-AUG58" --query_param "fields=id" | jq -r '.results[]|[.id] | @tsv' | xargs -I{} -n 1 stocks list datafilecopies {} | jq -r '.results[]|[.uri, .checksum, .status.value] | @tsv'
```

## For Developers
The tool is organized in packages:
- The `cli` module defines the different command line modules and commads
   - The entry point is the `cli/__main__.py` at the root
- The `stocks` module defines the STOCKS object model 
- The `stocks.assaysniffer` module defines the plugin framework for assay sniffers (see below)
   - New sniffers should be dropped in the `plugins` directory   
- The `stocksapi` module defines the STOCKS API and exposes it to the rest of the application via the `StocksManager`
   - The `StocksManager` accepts objects from the `stocks` object model
   - Internally, the `StocksManager` uses a low level `StocksClient` and encode/decode the API requests/responses using `Pydantic` objects
   - Pydantic objects should not be exposed to the rest of the app; they are only short term data objects 
- The `test` module regroups the unit tests
- The `utils.py` at the root is the place to define globally interesting constants, enums and methods


### Assay Sniffer Framework & Plugin
t.b.d