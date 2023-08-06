# Copernicus Marine Service client

A library to facilitate the access of Copernicus Marine Service products and datasets.

## Introduction

This package allows to recover products and datasets information from Command Line Interface or with Python code,
as well as download subsets and native files.

## Command Line Interface (CLI)

### Command *describe*
Retrieve information about products as JSON:

```
> copernicus-marine describe
{
  "products": [
    {
      "title": "Antarctic Sea Ice Extent from Reanalysis",
      "product_id": "ANTARCTIC_OMI_SI_extent",
      "thumbnail_url": "https://catalogue.marine.copernicus.eu/documents/IMG/ANTARCTIC_OMI_SI_extent.png",
      "production_center": "Mercator Oc\u00e9an International",
      "creation_datetime": "2018-02-12",
      "modified_datetime": "2018-02-12",
    }
    ...
  ]
}
```

Retrieve all information about datasets as JSON:

```
> copernicus-marine describe --include-datasets
{
  "products": [
    {
      "title": "Antarctic Sea Ice Extent from Reanalysis",
      "product_id": "ANTARCTIC_OMI_SI_extent",
      "thumbnail_url": "https://catalogue.marine.copernicus.eu/documents/IMG/ANTARCTIC_OMI_SI_extent.png",
      "production_center": "Mercator Oc\u00e9an International",
      "creation_datetime": "2018-02-12",
      "modified_datetime": "2018-02-12",
      "datasets": [
        {
          "dataset_id": "antarctic_omi_si_extent",
          "dataset_name": "antarctic_omi_si_extent",
          "services": [
            {
              "protocol": "ftp",
              "uri": "ftp://my.cmems-du.eu/Core/ANTARCTIC_OMI_SI_extent/antarctic_omi_si_extent"
            }
          ],
          "variables": []
        }
      ]
    },
    ...
  ]
}

```

Check out the help:

```
> copernicus-marine describe --help
Usage: copernicus-marine describe [OPTIONS]

Options:
  --one-line             Output JSON on one line
  --include-description  Include product description in output
  --include-datasets     Include product dataset details in output
  --include-keywords     Include product keyword details in output
  -c, --contains TEXT    Filter catalogue output. Returns products with
                         attributes matching a string token
  --overwrite-cache      Force to refresh the catalogue by overwriting the
                         local cache
  --help                 Show this message and exit.
```

### Command *login*

Create the configuration files for access to the copernicus marine service:
'.dodsrc', '.netrc', '.motuclient-python.ini'.
The directory to store these configuration files can be modified by the user using the "config-file-directory" option
but beware as it should also be passed to the *subset* and *native* command afterwards.
By default, if the configuration files already exist, the user is asked for confirmation to overwrite them.

Example:
'''
> copernicus marine login
< Username :
< Password :
> INFO     - root - Configuration files stored in ${HOME}\.copernicus_marine_client
'''


Checkout the help:
'''
> copernicus-marine login --help
Usage: copernicus-marine login [OPTIONS]

  This command creates the configurations files used by the various download
  services and store them in a directory that can be specified by the user. If
  the user specified a different 'config_file_directory' from default one
  ($HOME/.copernicus_marine_client), it needs to be passed also to the
  download commands.

  Examples:

  Case 1 (Recommended):

  With environment variables COPERNICUS_MARINE_CLIENT_USERNAME &
  COPERNICUS_MARINE_CLIENT_PASSWORD specified:

  > copernicus-marine login

  Case 2:

  > copernicus-marine login

  < Username: [USER-INPUT]

  < Password: [USER-INPUT]

  Case 3:

  > copernicus-marine login --username JOHN_DOE --password SECRETPASSWORD

  Case 4: Specific directory for config_files

  > copernicus-marine login --config-file-directory USER/SPECIFIED/PATH

Options:
  --username TEXT                 Search for environment variable:
                                  COPERNICUS_MARINE_CLIENT_USERNAME if not,
                                  ask for user input
  --password TEXT                 Search for environment variable:
                                  COPERNICUS_MARINE_CLIENT_PASSWORD if not,
                                  ask for user input
  --config-file-directory TEXT    Path to the directory where the
                                  configuration files are stored
  --assume-yes                    Flag to skip confirmation before overwriting
                                  configuration files
  --verbose [DEBUG|INFO|WARN|ERROR|CRITICAL|QUIET]
                                  Set the details printed to console by the
                                  command (based on standard logging library).
  --help                          Show this message and exit.
'''

### Command *subset*

Download a dataset subset, based on dataset id, variable names and attributes slices:

```
> copernicus-marine subset -i METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 -v analysed_sst -v sea_ice_fraction -t 2021-01-01 - T 2021-01-03 -x 0.0 -X 0.1 -y 0.0 -Y 0.1

< Username:
< Password:
< Trying to download as one file...
```

File downloaded to ./{dataset_id}.{nc/zarr} if not specified otherwise (through -o/--output-directory and -f/--output-filename options).

Check out the help:

```
> copernicus-marine subset --help

Usage: copernicus-marine subset [OPTIONS]

  Downloads subsets of datasets as NetCDF files or Zarr stores.     Either one
  of 'dataset-id' or 'dataset-url' is required     (can be found via the
  'copernicus-marine describe' command).     The arguments value passed
  individually through the CLI take precedence     over the values from the
  "motu-api-request" option, which takes precedence     over the ones from the
  "request-file" option

  Example:

    copernicus-marine subset --dataset-id METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
    --variable analysed_sst --variable sea_ice_fraction --start-datetime
    2021-01-01 --end-datetime 2021-01-02 --minimal-longitude 0.0 --maximal-
    longitude 0.1 --minimal-latitude 0.0 --maximal-latitude 0.1

    copernicus-marine subset -i METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 -v
    analysed_sst   -v sea_ice_fraction -t "2021-01-01 01:00:00" -T "2021-01-02
    13:00:00" -x 0.0 -X 0.1 -y 0.0 -Y 0.1

Options:
  -u, --dataset-url TEXT          The full dataset URL
  -i, --dataset-id TEXT           The dataset id
  --username TEXT
  --password TEXT
  -v, --variable TEXT             Specify dataset variables
  -x, --minimal-longitude FLOAT RANGE
                                  Minimal longitude for the subset. Requires a
                                  float within this range:  [-180<=x<=180]
  -X, --maximal-longitude FLOAT RANGE
                                  Maximal longitude for the subset. Requires a
                                  float within this range:  [-180<=x<=180]
  -y, --minimal-latitude FLOAT RANGE
                                  Minimal latitude for the subset. Requires a
                                  float within this range:  [-90<=x<=90]
  -Y, --maximal-latitude FLOAT RANGE
                                  Maximal latitude for the subset. Requires a
                                  float within this range:  [-90<=x<=90]
  -z, --minimal-depth FLOAT RANGE
                                  Minimal depth for the subset. Requires a
                                  float within this range:  [x>=0]
  -Z, --maximal-depth FLOAT RANGE
                                  Maximal depth for the subset. Requires a
                                  float within this range:  [x>=0]
  -t, --start-datetime [%Y|%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  The start datetime of the temporal subset.
                                  Caution: encapsulate date with " " to ensure
                                  valid format for format "%Y-%m-%d %H:%M:%S"
  -T, --end-datetime [%Y|%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  The end datetime of the temporal subset.
                                  Caution: encapsulate date with " " to ensure
                                  valid format for format "%Y-%m-%d %H:%M:%S"
  -o, --output-directory PATH     The destination folder for the downloaded
                                  files. Default is the current directory
  -f, --output-filename PATH      Concatenate the downloaded data in the given
                                  file name (under the output directory)
  --assume-yes                    Flag to skip confirmation before download
  --force-protocol [zarr|zarr-map|zarr-timeserie|opendap|motu]
                                  Force download through one of the available
                                  protocols
  --dry-run                       Flag to specify NOT to send the request to
                                  external server. Returns the request instead
  --request-file PATH             Option to pass a filename corresponding to a
                                  file containg CLI arguments. The file MUST
                                  follow the structure of dataclass
                                  'SubsetRequest'.
  --motu-api-request TEXT         Option to pass a complete MOTU api request
                                  as a string. Caution, user has to replace
                                  double quotes " with single quotes ' in the
                                  request
  --log-level [DEBUG|INFO|WARN|ERROR|CRITICAL|QUIET]
                                  Set the details printed to console by the
                                  command (based on standard logging library).
  --help                          Show this message and exit
```

### Command *native*

Download a native file (or files), based on dataset id or path to files:

Example:
```
> copernicus-marine native -u ftp://my.cmems-du.eu/Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/

< Username:
< Password:
< You requested the download of the following files:
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202207.nc - 3.27 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202208.nc - 3.29 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202209.nc - 3.28 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202210.nc - 3.26 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202211.nc - 3.26 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202212.nc - 3.26 MB

Total size of the download: 19.62 MB


Do you want to continue? [y/N]:
```

File(s) downloaded to ./{path}/{filename} if not specified otherwise:
- "--output-path" specifies a directory to dump the files in
- "--no-directories" to not recreate the folder structure

If not specified otherwise, after the header display with a summary of the request,
the user is asked for confirmation:
- "--no-confirmation" to turn down the confirmation prompt
- "--show-outputnames" to display the full paths of the outputs files

Check out the help:

```
> copernicus-marine native --help

Usage: copernicus-marine native [OPTIONS]

  Downloads native data files based on     dataset_id or datafiles url path.
  The function fetches the files recursively if a folder path is passed as
  url.     When provided a dataset id,     all the files in the corresponding
  folder will be downloaded.

      By default for any download request, a summary of the request result is
      displayed to the user and a confirmation is asked.     This can be
      turned down. Example:

    copernicus-marine native -nd -o data_folder --dataset-id
    cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m

    copernicus-marine native -nd -o data_folder --dataset-url
    ftp://my.cmems-du.eu/Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-
    pft_myint_7km-3D-diato_P1M-m

Options:
  -u, --dataset-url TEXT       Path to the data files
  -i, --dataset-id TEXT        The dataset id
  --username TEXT
  --password TEXT
  -nd, --no-directories        Option to not recreate folder hierarchy in
                               ouput directory.
  --show-outputnames           Option to display the names of the output files
                               before download.
  -o, --output-directory PATH  The destination directory for the downloaded
                               files. Default is the current directory
                               [required]
  --assume-yes                 Whether to ask for confirmation before
                               download, after header display. If 'True',
                               skips confirmation.
  --dry-run                    Flag to specify NOT to send the request to
                               external server. Returns the request instead
  --request-file PATH          Option to pass a file containg CLI arguments.
                               The file MUST follow the structure of dataclass
                               'SubsetRequest'. ANY PARAMETER SPECIFIED ASIDE
                               FROM FILE WILL NOT BE TAKEN INTO CONSIDERATION
                               FOR THE REQUEST IF FILE IS SPECIFIED.
  --help                       Show this message and exit.
```

## Python functions

The library also provide python functions to help with catalogue
browsing and datasets download in scripts.

### Basic example:

In this example 4 steps are performed:
  1- Fetch the catalogue to select a dataset
  2- Construct a SubsetRequest for this dataset
  3- Download the subset as a zarr store
  4- Open the subset as an xarray dataset

```
import copernicus_marine_client as cmc

# Step 1: Fetch catalogue and parse information on dataset
catalogue = cmc.fetch_catalogue()
dataset_id = 'cmems_mod_ibi_bgc_anfc_0.027deg-3D_P1D-m'
assert(dataset_id in cmc.get_all_dataset_ids())
dataset = catalogue.filter([dataset_id]).products[0].datasets[0]
# Object "dataset" can be used to display all the metadata necessary to build a SubsetRequest
variable = [variable for variable in dataset.variables if variable.short_name in ['zooc']][0]
coordinates = {coordinate.coordinates_id: (coordinate.minimum_value, coordinate.maximum_value) for coordinate in variable.coordinates}

# Step 2: Construct the request based on parsed information
subset_request = cmc.SubsetRequest(
  dataset_id='cmems_mod_ibi_bgc_anfc_0.027deg-3D_P1D-m',
  start_datetime="2023-04-20",
  end_datetime='2023-04-21',
  minimal_latitude= 30.0,
  maximal_latitude=30.1,
  minimal_longitude=0.1,
  maximal_longitude=0.2,
  minimal_depth=100,
  maximal_depth=1000,
  variables = ['zooc'],
  force_protocol = "zarr-map",
  output_directory = 'data_folder',
  output_filename = 'datastore.zarr',
  assume_yes = True,
)

# Step 3: Download the subset based on request content
filename = cmc.download_subset(username='FAKE_USERNAME', password='FAKE_PASSWORD', subset_request=subset_request)

# Step 4: Open the downloaded subset as an xarray dataset
subset = cmc.open_dataset(filepath=filename, engine='zarr', out_type='xarray')
```

## Installation

Using pip, for example:
```
pip install copernicus-marine-client
```
## Technical details

This module is organized around two capabilities:
- a catalogue, parsed from web requests, that contains informations on the available datasets
- a downloader, to simplify the download of dataset files or subsets

The catalogue can be displayed by the user and is used by the downloader to link the user
requests with files or subset of files to retrieve.
The downloader will help the user download the needed datasets.

A rigid format, specified in "request_structure.py" is used to ensure conformity of the information passed between the CLI command and the python functions.

For subset command, the format is:

```
@dataclass
class SubsetRequest:
    dataset_url: Optional[str] = None
    dataset_id: Optional[str] = None
    variables: Optional[List[str]] = None
    minimal_longitude: Optional[float] = None
    maximal_longitude: Optional[float] = None
    minimal_latitude: Optional[float] = None
    maximal_latitude: Optional[float] = None
    minimal_depth: Optional[float] = None
    maximal_depth: Optional[float] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    output_directory: Optional[str] = None
    output_filename: Optional[str] = None
    assume_yes: Optional[bool] = None
    force_protocol: Optional[str] = None
    dry_run: Optional[bool] = None
```
