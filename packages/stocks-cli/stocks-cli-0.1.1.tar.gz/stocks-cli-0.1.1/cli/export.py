# -*- coding: utf-8 -*-
"""
The 'export' module of the CLI
"""
import csv
import glob
import io
import os
import shutil
import sys
import zipfile
from enum import Enum
import datetime
from pathlib import Path

import numpy as np
import requests
import pytz
import pandas as pd
import getpass
import re

import typer

from cli.export_eln_website_utils import get_experiment_export_dirname, build_static_web_site_for_eln_export
from cli import get_default_config_file_path
from stocks.models import Study, Assay, Protocol, SequencingAssay, Experiment, Project, DatasetFileCopy, \
    AnnotationType, UserGroup
from stocksapi.client import StocksClient
from stocksapi.manager import StocksManager
from stocksapi.models import *
from cli.export_utils import COMMENT_STOCKS_UUID, MAGETAB_RELEASE_DATE, \
    StudyExportFormat, add_default_submitter, add_owner_role, extract_protocol_list, extract_final_annotations, \
    write_df_in, create_annofactor_df, create_protocol_ref, create_idf_design, create_idf_experimental_factors, \
    create_idf_users, create_idf_protocol, add_user_institutions, owner_name, runtype_layout_map, \
    check_table_bools, stocks_annotare_library_contruction_map, single_cell_annotare_fillin, \
    MAGETAB_HEADER_SINGLE_CELL_ANNOTARE, merge_df_columns, to_ena_format, get_export_table, process_assays, \
    create_fake_data, ENA_TABLES_NAME, upload_ena_annotation, ena_credentials_file, parse_receipt, _ena_upload_cli, \
    ANNOTATION_STOCKS_ENA_STUDY, TODO, TERM_SOURCE_REF, QUALITY_SCORING_SYSTEM, LIBRARY_ENCODING, ASCII_OFFSET, \
    StudyValidationReport, write_report_file, Report, parse_html
from cli.config import get_config
from cli.utils import ModelType, HTMLFilter

logger = logging.getLogger(__name__)

# name of this module (as appearing on the command line) is the last part of the __name__ eg cli.config -> config
_MODULE_NAME = __name__.rsplit(".", 1)[-1]
# list of command names offered in this module
_CMD_EXPORT_ELN = "eln"
_CMD_EXPORT_STUDY = "study"
_CMD_EXPORT_LOGS = "usagelogs"
_CMD_EXPORT_LINKS = "links"
_CMD_SUBMIT_ENA = "ena"
_CMD_UPLOAD_ACCESSION = "upload"


# enums for fixed choices
class ResolutionEnum(str, Enum):
    DAY = "day"
    MONTH = "month"
    YEAR = "year"


# create the CLI app
app = typer.Typer()


# @app.command("test")
# def test(conf_file_path: str = typer.Option(
#     get_default_config_file_path(),
#     "--config-path",
#     help="Config file absolute path")
# ) -> None:
#     """
#     wipe the config file
#     """
#     client: StocksClient = StocksClient(get_config(Path(conf_file_path)))
#     stocks_manager: StocksManager = StocksManager(client)
#     d = stocks_manager.list_dropboxes(for_username="girardot")
#     print(d)

@app.command(_CMD_EXPORT_LOGS, help="Export the user connection statistics")
def export_usage_logs(
        output: Path = typer.Option(
            None,
            "--file_path",
            "-o",
            help="Output file path (should not exist)"
        ),
        start_date: datetime = typer.Option(
            datetime(datetime.now().year, 1, 1),
            "--start_date",
            "-f",
            formats=["%Y-%m-%d"],
            help="Usage logs starting from this date"
        ),
        end_date: datetime = typer.Option(
            datetime.now().strftime("%Y-%m-%d"),
            "--end_date",
            "-e",
            formats=["%Y-%m-%d"],
            help="Usage logs starting till this date"
        ),
        resolution: ResolutionEnum = typer.Option(
            "Day",
            "--resolution", "-r",
            case_sensitive=False,
            help="Group user count per day, month or year"),
        aggregate: bool = typer.Option(
            True,
            help="Aggregate user counts. If set to false, a row per unique user is returned."
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path"
        )
):
    """
    Admin only.
    Get the number of active users for given time frame. Returned as csv file or json stdout.
    OUTPUT must be specified as a .xls(x) or csv file to retrieve an excel or csv format.

    - start_date: e.g. 2021-01-27
    - end_date: e.g. 2021-12-31
    - resolution: day/month/year
    """

    # check file_path file does not exist
    if output and output.exists():
        raise typer.BadParameter(f"Output file already exists, please remove first: {str(output)}")

    # Initiate client and manager.
    client: StocksClient = StocksClient(get_config(Path(conf_file_path)))
    stocks_manager: StocksManager = StocksManager(client)

    try:
        o_format = _determine_output_format(file_path=output)
        if not o_format or o_format == "json":
            data = stocks_manager.fetch_usage_logs(start_date, end_date, resolution.value, aggregate)
        elif o_format == "csv":
            data = stocks_manager.fetch_usage_logs_csv_table(start_date, end_date, resolution.value, aggregate)
        else:
            data = stocks_manager.fetch_usage_logs_excel_table(start_date, end_date, resolution.value, aggregate)

        if output:
            outfile = open(output, "wb")
            outfile.write(data)
            outfile.close()
        else:
            print(data)
    except PermissionError as err:
        print(str(err))


@app.command(_CMD_UPLOAD_ACCESSION, help="Directly uploads the accession numbers from the XML receipt file of an ENA "
                                         "submission to the corresponding stocks items.")
def upload_accession(
        receipt_path: str = typer.Option(
            ...,
            "--receipt",
            "-r",
            help="Path to the XML receipt file from the ENA"
        ),
        study_id: str = typer.Option(
            None,
            "--study",
            "-s",
            help="The UUID of the study"
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path"
        )
) -> None:
    # Initiate client and manager.
    client: StocksClient = StocksClient(get_config(Path(conf_file_path)))
    stocks_manager: StocksManager = StocksManager(client)

    # Checks
    if not Path(receipt_path).exists():
        raise typer.BadParameter(f"Could not find file at {receipt_path}")
    # Checks reading rights
    if not os.access(receipt_path, os.R_OK):
        raise typer.BadParameter(f"You do not have reading rights at: {receipt_path}")

    upload_accessions(receipt_path, stocks_manager, study_id)


@app.command(_CMD_SUBMIT_ENA, help="Submit to the ENA a study metadata already locally exported")
def submit_ena(
        export_dir: str = typer.Option(
            ...,
            "--odir",
            "-o",
            help="Path to where the metadata tables to be submitted to the ENA are present. "
                 "Directory should contain all 4 tables to be exported. Table names should be formated as: "
                 "'ena_[study | run | samples | experiment]_[study_id].tsv'. If the folder contains tables belonging to"
                 " several different studies, providing the study id is necessary."
        ),
        study_id: str = typer.Option(
            None,
            "--study",
            "-s",
            help="The UUID of the study to submit, in case several different studies "
                 "in enatable format have been exported in the same folder"
        ),
        execute: bool = typer.Option(
            False,
            '--execute / --dry-run',
            help="Use --dry-run to test the submission against the ENA sandbox endpoint "
                 "(uses fake data files e.g. FastQ); in this mode ENA accession numbers will not be loaded in STOCKS. "
                 "Use --execute to perform the submission for real."
        ),
        ena_username: str = typer.Option(
            None,
            '--username',
            '-u',
            help=f"ENA Webin username for submission. Not recommended over providing a credential file"
        ),
        ena_password: str = typer.Option(
            None,
            '--password',
            '-p',
            help=f"ENA Webin password for submission. Not recommended over providing a credential file"
        ),
        ena_credentials: str = typer.Option(
            None,
            '--credentials',
            '-c',
            help=f"Path to a yaml file containing ENA submission credentials"
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path"
        )
) -> None:
    """
    Submit to the ENA tables which have already been locally exported by the export study command line. This command
    does not redo any table content checks and does not support any other use cases.
    Tables name need to be formatted as is:
    'ena_[study | run | samples | experiment]_[study_id].tsv'
    """

    # Initiate client and manager.
    client: StocksClient = StocksClient(get_config(Path(conf_file_path)))
    stocks_manager: StocksManager = StocksManager(client)

    # Checks
    # check export dir_path
    if Path(export_dir).exists() is False:
        raise typer.BadParameter(f"No dir at: {export_dir}")
    # Checks writing rights
    if not os.access(export_dir, os.W_OK):
        raise typer.BadParameter(f"You do not have writing rights at: {export_dir}")

    # Initiate/check folders and files
    export_dir = os.path.abspath(export_dir).strip()  # subprocess.call() doesnt handle relative paths
    receipt = os.path.join(export_dir, 'receipt.xml')
    if Path(receipt).exists():
        raise typer.BadParameter(f"Receipt file already exists, please remove: {receipt}")
    if study_id:
        ena_files_path = {}
        check = False
        for name in ENA_TABLES_NAME:
            p = os.path.join(export_dir, f'ena_{name}_{study_id}.tsv')
            if Path(p).exists():
                ena_files_path[name] = p
                check = True  # Check if at least one file is present
        if not check:
            raise FileNotFoundError(f"No files with format 'ena_[sample|run|experiment|study]_{study_id}.tsv' was found"
                                    f" in {export_dir}")
    else:
        ena_files_path = {}
        for name in ENA_TABLES_NAME:
            file_path = os.path.join(export_dir, f'ena_{name}_*.tsv')
            table_list = glob.glob(file_path)
            if len(table_list) > 1:
                raise FileExistsError(f"Ambiguous file name error: several files corresponding to ena_{name}_*.tsv have"
                                      f" been found. Please add a --study id or clean the directory.")
            if len(table_list) == 1:
                ena_files_path[name] = table_list[0]
        if not ena_files_path:
            raise FileNotFoundError(f"No files with format 'ena_[sample|run|experiment|study]_*.tsv' was found"
                                    f" in {export_dir}")

    # Get ENA credential from yaml file or temporarily create one in the export folder.
    if bool(ena_username) != bool(ena_password):  # Tests if both arguments are given or not given.
        raise typer.BadParameter(f"You must provide either both or none of the username and password")
    ena_cred_path, to_del_credentials = ena_credentials_file(ena_username, ena_password, ena_credentials,
                                                             os.path.dirname(conf_file_path), export_dir)
    if not ena_cred_path:
        raise typer.BadParameter(f"No credentials for an ENA submission where provided and no file could be "
                                 f"found")
    # ENA submission
    ena_submission(export_dir, study_id, ena_files_path, ena_cred_path, to_del_credentials, execute, stocks_manager)


@app.command(_CMD_EXPORT_STUDY, help="Export study and associated datasets metadata")
def export_study(
        study_id: str = typer.Option(
            ...,
            "--study",
            "-s",
            help="The UUID of the study to export "
        ),
        format: StudyExportFormat = typer.Option(
            StudyExportFormat.magetab,
            "--format",
            case_sensitive=False,
            help="Export format to use. 'Enatables' is only relevant to prepare ENA submission"
        ),
        export_dir: str = typer.Option(
            ...,
            "--odir",
            "-o",
            help="Path to where the study should be exported"
        ),
        filename: str = typer.Option(
            "magetab.csv",
            "--filename",
            "-f",
            help=f"The export filename (will be created in --odir). Only relevant when format is "
                 f"{StudyExportFormat.magetab}"
        ),
        stocks_comments: bool = typer.Option(
            True,
            "--stocks-comments/--no-stocks-comments",
            help=f"If given --stocks-comments and format is {StudyExportFormat.magetab}, will add information from "
                 f"stocks as comments to the magetab. --no-stocks-comments will omit them"
        ),
        submit: bool = typer.Option(
            False,
            "--submit",
            help=f"Submit to the ENA directly after exporting the ENA tables. Only relevant when format is "
                 f"{StudyExportFormat.enatables}. If --execute is not enabled, will only submit to a temporary ENA "
                 f"endpoint and will not update STOCKS accession numbers."
        ),
        execute: bool = typer.Option(
            False,
            '--execute / --dry-run',
            help="--dry-run: Test submission to ENA sandbox endpoint with simulated fake data. Does not update STOCKS "
                 "with the accession numbers"
                 "--execute: Submit to ENA proper. Updates STOCKS with the accession numbers."
        ),
        ena_username: str = typer.Option(
            None,
            '--ena-username',
            help=f"ENA Webin username for submission. Only relevant when format is {StudyExportFormat.enatables} and "
                 f"--submit is given. Not recommended over providing a credential file"
        ),
        ena_password: str = typer.Option(
            None,
            '--ena-password',
            help=f"ENA Webin password for submission. Only relevant when format is {StudyExportFormat.enatables} and "
                 f"--submit is given. Not recommended over providing a credential file"
        ),
        ena_credentials: str = typer.Option(
            None,
            '--ena-credentials',
            help=f"Path to a yaml file containing ENA submission credentials. Only relevant when format is "
                 f"{StudyExportFormat.enatables}, --submit is given, and a --username and --password have not been "
                 f"provided"
        ),
        filter_sub: bool = typer.Option(
            True,
            '--ena-filter / --ena-no-filter',
            help="--ena-no-filter: Writes tables with ENA formatting while keeping the rows that already have accession"
                 " numbers. The tables will contain columns with accession numbers. If this is enabled and some items "
                 "are already present in the ENA database, any ENA submission will fail."
                 "--ena-filter: Writes tables for ENA submission and omits rows for items which already have accession "
                 "numbers."
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path"
        )
) -> None:
    """
    Export from STOCKS the study metadata according to a given study_id.\n
    The format of the export will be determined by the format parameter:\n
    - 'tabular' format will create a file containing various information for
        each samples of the study relevant for most submission purposes.\n
    - 'magetab' will create a file containing a IDF and a SDRF table with the relevant information for a
        BioStudies/Annotare submission.\n
    - 'enatables' will create up to 4 different tables according to the format required by the "ena-upload-cli".
        If --submit parameter enabled, will submit those tables to the ENA and update the STOCKS items with their
        given accession code. Submission will only work if the datafiles have already been uploaded to the ENA.
        Annotates items with their corresponding ENA accession numbers.
        File name format: 'ena_[study | run | samples | experiment]_[study_id].tsv'
    Default: 'magetab'
    """
    # Initiate client and manager.
    client: StocksClient = StocksClient(get_config(Path(conf_file_path)))
    stocks_manager: StocksManager = StocksManager(client)

    # Checks
    # check export dir_path
    Path(export_dir).mkdir(parents=True, exist_ok=True)
    if Path(export_dir).exists() is False:
        raise typer.BadParameter(f"Failed to create dir_path at: {export_dir}")
    # Checks writing rights
    if not os.access(export_dir, os.W_OK):
        raise typer.BadParameter(f"You do not have writing rights at: {export_dir}")

    # Initiate/check folders and files
    # filename is required for some export format
    if format == StudyExportFormat.magetab or format == StudyExportFormat.tabular:
        if filename == "" or filename is None:
            raise typer.BadParameter(f"A filename is expected when export format is: {format}")
        # check file does not already exist
        outpath: Path = Path(export_dir, filename)
        if outpath.exists():
            raise typer.BadParameter(f"File already exists, please remove: {str(outpath)}")
    elif format == StudyExportFormat.enatables:
        export_dir = os.path.abspath(export_dir) + '/'  # subprocess.call() doesnt handle relative paths
        ena_file_outpath = [f"{export_dir}ena_{t}_{study_id}.tsv" for t in ENA_TABLES_NAME]
        for f in ena_file_outpath:
            if Path(f).exists():
                raise FileExistsError(f"File already exists, please remove: {str(f)}")
        if submit:
            # Get ENA credential from yaml file or create one in the export folder.
            if bool(ena_username) != bool(ena_password):  # Tests if both arguments are given or not given.
                raise typer.BadParameter(f"You must provide either both or none of the username and password")
            ena_cred_path, to_del_credentials = ena_credentials_file(ena_username, ena_password, ena_credentials,
                                                                     os.path.dirname(conf_file_path), export_dir)
            if not ena_cred_path:
                raise typer.BadParameter(f"No credentials for an ENA submission where provided and no file could be "
                                         f"found")
            receipt = os.path.join(export_dir, 'receipt.xml')
            if Path(receipt).exists():
                raise typer.BadParameter(f"Receipt file already exists, please remove: {receipt}")

    # Check given id is really a study
    study: Study = stocks_manager.fetch_study(study_id, load_ownership=True)
    if not study:
        raise typer.BadParameter(f"Wrong value provided for --study, no study returned for UUID {study_id}")
    # End checks

    # Parse HTML description
    study.description = parse_html(study.description)

    # Export raw metadata table
    if format == StudyExportFormat.tabular:
        o_format = _determine_output_format(file_path=outpath)
        if o_format not in ["xlsx", "csv"]:
            raise typer.BadParameter(f"Wrong file extension (--filename), must be .xlsx or .csv: {str(outpath)}")
        elif o_format == "csv":
            data = stocks_manager.fetch_study_dataset_csv_table(study_id)
        else:
            data = stocks_manager.fetch_study_dataset_excel_table(study_id)
        outfile = open(outpath, "wb")
        outfile.write(data)
        outfile.close()
    # End of table export

    if format == StudyExportFormat.magetab or format == StudyExportFormat.enatables:
        val_report = StudyValidationReport(study)
        # get my raw export table into a pandas DataFrame
        table: pd.DataFrame = get_export_table(study_id, stocks_manager)

        # Extract protocols objects from raw table and add them to study object
        study.protocols: List[Protocol] = extract_protocol_list(table, stocks_manager)
        if not study.protocols:
            logger.warning(f"No protocols have been fetched from the arrayexpress export protocol list."
                           f"Study ID:{study_id}")

        assay_dict, assay_type = process_assays(table, study, stocks_manager)  # Assays as protocols

        # Extract final annotations
        annotations_dict: dict = extract_final_annotations(table, stocks_manager.list_annotation_types())
        study.experimental_factors: list[str] = [x for x in annotations_dict if annotations_dict[x]["is_factor"]]

        val_report.validate_annotations(table)
        val_report.validate_protocols(table, study)
        val_report.validate_data(table)

        if format == StudyExportFormat.magetab:
            add_default_submitter(study)  # add default submitter first to the study
            add_owner_role(study)  # add owmer as usermember
            add_user_institutions(study)  # add users default institution
            val_report.validate_study(study)

            # Write file
            report = Report(val_report)
            report.magetab_report()
            write_report_file(report, export_dir)
            sdrf: pd.DataFrame = create_sdrf(table, study, assay_dict, annotations_dict, stocks_comments)
            create_magefile(outpath, table, study, assay_dict, sdrf, stocks_comments=stocks_comments)

        if format == StudyExportFormat.enatables:
            # ENA tables creation
            tables = to_ena_format(table, study, assay_type, assay_dict, annotations_dict, stocks_manager, filter_sub)
            final_outpath = {}
            for t, p in zip(tables, ena_file_outpath):
                if t is not None and not t.empty:
                    final_outpath[os.path.basename(p).split('_')[1]] = p
                    t.to_csv(p, header=True, index=False, sep="\t")
            if not final_outpath:
                raise ValueError("No ENA format tables have been exported")

            # ENA submission
            if submit:
                ena_submission(export_dir, study_id, final_outpath, ena_cred_path, to_del_credentials, execute,
                               stocks_manager)


@app.command(_CMD_EXPORT_LINKS, short_help="Create symbolic links to data files.",
             help="The command retrieves all datasets of a project, study, assay, dataset collection or dataset and "
                  "tries to create symbolic links in the current dir. Note that links can only be created for the "
                  "datasets you have access to and that are located on the local network")
def symlink(
        project: str = typer.Option(
            None,
            "--project",
            "-p",
            help="Get datafiles of the specified project id"
        ),
        study: str = typer.Option(
            None,
            "--study",
            "-s",
            help="Get datafiles of the specified study id"
        ),
        assay: str = typer.Option(
            None,
            "--assay",
            "-a",
            help="Get datafiles of the specified assay id"
        ),
        collection: str = typer.Option(
            None,
            "--collection",
            "-c",
            help="Get datafiles of the specified collection id"
        ),
        dataset: str = typer.Option(
            None,
            "--dataset",
            "-d",
            help="Get datafiles of the specified dataset id"
        ),
        primary: bool = typer.Option(
            True,
            "--primary / --all",
            help="Only fetches the primary copy of datafiles; else return all copies"
        ),
        target_dir: Path = typer.Option(
            Path(os.getcwd()),
            "--target-dir",
            "-t",
            help="Path to a directory where the links should be created"
        ),
        lnk_name_template: str = typer.Option(
            None,
            "--link-name-formulae",
            "-f",
            help="An template formulae to build link name, e.g. '{Sample}_{Read Type}.fastq.gz', where the {X} "
                 "placeholders will be replaced by matching metadata value e.g. '{Sample}' is replaced by the sample name"
                 "and {Read Type} by the read number."
                 "Note that 'X' must match, case-sensitively, column headers of the data file metadata table. "
                 "While some column headers are always available, others are context specific e.g. annotations, assay "
                 "type... you can learn which headers are available in your context with --list-data-headers"
        ),
        list_metadata_fields: bool = typer.Option(
            False,
            "--list-data-headers / --no-list-data-headers",
            help="List all column headers of the data file metadata table available in your context, and quit (no links"
                 " created). This option will only list columns with values in case --reduce is used. "
                 "The data file metadata table is also saved under name "
                 "'datafiles_metadata_for_<context_item_type>_<uuid>.csv'."
                 " This is mainly helpful to help you assembling a -link-name-formulae when building the command line."
        ),
        reduce: bool = typer.Option(
            True,
            "--reduce / --keep-empty-columns",
            help="When the data file metadata table is exported, this option makes sure columns only holding empty "
                 "strings or NaN are removed from the table."
        ),
        meta_table: str = typer.Option(
            "data_info.txt",
            "--meta-table",
            "-m",
            help="Name of a tabular txt file containing additional information about the data files"
        ),
        resume: bool = typer.Option(
            False,
            "--resume",
            "-r",
            help="Skip symlinks if they already exists. If False, exit on finding an existing link."
        ),
        query_params: List[str] = typer.Option(
            None,
            "--query_param", "-q",
            help="Filter request by these query parameters e.g. --filter name=blah."
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path"
        )
) -> None:

    if target_dir in [None, "."]:
        target_dir = Path()
        logger.debug(f"Target directory set to {str(target_dir)}")
    else:
        target_dir = Path(target_dir)

    # make sure target dir exists
    target_dir.mkdir(parents=True, exist_ok=True)

    client: StocksClient = StocksClient(get_config(Path(conf_file_path)))
    stocks_manager: StocksManager = StocksManager(client)

    # the filter below is not yet avail and will be ignored by the server
    # we still have it here for when it becomes avail
    # for now, we set only_count=False in _list_items() calls and post-filter
    if primary:
        if not query_params:
            query_params = list()
        else:
            query_params = list(query_params)
        query_params.append(f"is_primary_copy=True")
    elif lnk_name_template:
        raise typer.BadParameter(
            f"--formulae can only be used when linking to primary data copies i.e. not with --all.")

    # use singular form in filter_type, we have only_count set to False to be able to post filter
    if study:
        filter_uuid = study
        expected_type = "study"
    elif project:
        filter_uuid = project
        expected_type = "project"
    elif assay:
        filter_uuid = assay
        expected_type = "assay"
    elif dataset:
        filter_uuid = dataset
        expected_type = "dataset"
    elif collection:
        filter_uuid = collection
        expected_type = "datasetcollection"
        # not sure this works
    else:
        raise typer.BadParameter(f"one of --project, --study, --assay, --collection or --dataset must be provided")

    # check uuid is for indicated type
    filter_type = _check_item_type(stocks_manager=stocks_manager, uuid=filter_uuid, expected_type=expected_type)
    # fetch data now
    filecopies: List[DatasetFileCopy] = stocks_manager.list_datafilecopies(filter_type=filter_type,
                                                                           filter_uuid=filter_uuid,
                                                                           only_primary_copy=primary)

    use_subpath_for_uniqueness: bool = False

    # do we have custom link name, if so validate
    custom_lnk_names = {}
    # a dict storing all the individual datasetfile a link should be created and whether it was successfully created
    all_datasetfile_path: Dict[str, bool] = {}
    if lnk_name_template or list_metadata_fields:
        # fetch all dataset meta
        dataset_meta = stocks_manager.fetch_dataset_metatable(uuid=filter_uuid)
        # convert to panda DF
        metatable = pd.read_table(
            io.BytesIO(dataset_meta), dtype=str, sep=",", keep_default_na=False).fillna('').astype(str)
        if reduce:
            metatable.replace('', np.nan, inplace=True)
            # drop empty columns
            metatable.dropna(axis=1, how='all', inplace=True)

        metatable.to_csv(Path(target_dir, f"datafiles_metadata_for_{expected_type}_{filter_uuid}.csv"), index=False)

        if list_metadata_fields:
            print(f"Available headers in this data context: {list(metatable)}")
            sys.exit()

        p = re.compile(r'{([^{}]+)}', re.IGNORECASE)
        headers = p.findall(lnk_name_template)
        # check headers are in the metatable
        missing_headers = []
        for h in headers:
            if h not in list(metatable):
                missing_headers.append(h)

        if missing_headers:
            raise typer.BadParameter(f"placeholders {missing_headers} of the link name formulae {lnk_name_template} are"
                                     f" not found in the available metadata : {list(metatable)}")

        # compute the link names keyed by the full file path
        all_links = {}

        for index, row in metatable.iterrows():
            row_map = row.to_dict()
            lnk_name = lnk_name_template.format(**row_map).strip().replace(' ', '_')
            datasetfile_path: str = row_map['FilePath']
            # datafiles can be repeated in many lines (eg different channels), we skip if already seen
            if datasetfile_path not in all_datasetfile_path:
                all_datasetfile_path[datasetfile_path] = False
            else:
                continue
            custom_lnk_names[datasetfile_path] = lnk_name
            if lnk_name in all_links:
                raise typer.BadParameter(
                    f"Using the link name formulae {lnk_name_template} does not produce a unique link name per data "
                    f"file/folder. For example the link name {lnk_name} would point to both {row_map['FilePath']} and "
                    f"{all_links[lnk_name]}. Please review your formulae.")
            all_links[lnk_name] = datasetfile_path
        logger.debug(custom_lnk_names)
    else:
        # we check if all link names are unique
        link_names = set()
        for dfc_res in filecopies:
            # we would normally use link to dfc_res.shortname directly --if this results in unique names
            if dfc_res.shortname in link_names:
                use_subpath_for_uniqueness = True
                break
            link_names.add(dfc_res.shortname)

    info = []
    info_headers = ["shortname", "linkname", "uri", "is_primary_copy", "copy_id", "dataset_id"]

    for dfc_res in filecopies:
        logger.warning(dfc_res.uri)
        # by default get the no formulae link name
        lnk_name: str = _get_run_dir_relpath(dfc_res) if use_subpath_for_uniqueness else dfc_res.shortname
        if lnk_name_template:
            # then get the custum name
            lnk_name = custom_lnk_names[dfc_res.uri]
        target_path = Path(target_dir, lnk_name)

        dfc_info = {'shortname': dfc_res.shortname, 'linkname': lnk_name, 'uri': dfc_res.uri,
                    'is_primary_copy': dfc_res.is_primary_copy, 'copy_id': dfc_res.id,
                    'dataset_id': dfc_res.dataset if isinstance(dfc_res.dataset, str) else dfc_res.dataset.id
                    }
        info.append(dfc_info)

        target_path.parent.mkdir(exist_ok=True, parents=True)
        logger.info(f"Linking {dfc_res.uri} -> {target_path}")
        try:
            target_path.symlink_to(dfc_res.uri)
        except FileExistsError:
            if resume:
                logger.info("Symlink already exists, skipping.")
            else:
                logger.critical("Symlink already exists, exiting! Choose another target directory or use "
                                "--skip-existing to continue.")
                sys.exit(1)
    if not info:
        print("No data files returned for parameters")
        sys.exit(1)

    if meta_table:
        with open(target_dir / meta_table, "w") as info_fh:
            writer = csv.DictWriter(info_fh, fieldnames=info_headers,
                                    delimiter="\t")
            writer.writeheader()
            writer.writerows(info)
    print("Successfully created symlinks.")


def _get_run_dir_relpath(dfc: DatasetFileCopy) -> str:
    """
    extract the sub path from the run directory. This process is driven by the assumption that the STOCKS repo is like
    .../Data/Assay/<technology>/<year>/<run_dir> or .../Data/Other/<year>/<session_dir>
    :param dfc:
    :return:
    """

    # uri eg '/g/hentze/STOCKS/Data/Assay/sequencing/2019/2019-05-27-HKC5TBGXB/lane1/LIB44347_RBA43830/fastq/HKC5TBGXB_T3_ProtA_input_2_19s002191-1-1_Asencio-Salcedo_lane119s002191_2_sequence.txt.gz'
    if '/Data/Assay/' in dfc.uri:
        run_dir = dfc.uri.split(sep='/Data/Assay/')[1].split('/')[2]
        # run_dir -> 2019-05-27-HKC5TBGXB
        p = dfc.uri.split(sep=run_dir)[1].lstrip("/")
        if 'sequencing' in dfc.uri:
            # in case of sequencing, we also have legacy situation with sub dir like '../lane1/LIB44347_RBA43830/fastq/'
            # which we can skip
            p = re.sub(r'lane\d+/LIB\d+_RBA\d+/fastq/', "", p)
    elif '/Data/Other/' in dfc.uri:
        run_dir = dfc.uri.split(sep='/Data/Other/')[1].split('/')[2]
        p = dfc.uri.split(sep=run_dir)[1].lstrip("/")
    else:
        logger.warning(f"File path does not match STOCKS repo architecture: {dfc.uri} ")
        p = ""

    return str(Path(run_dir, p))


def _check_item_type(stocks_manager: StocksManager, uuid: str, expected_type: str) -> str:
    """

    :param stocks_manager: a fully init manager
    :param uuid: the uuid to check
    :param expected_type: the expected type
    :return: the validated type if check is successful or raise typer.BadParameter
    """
    data = stocks_manager.resolve(uuid=uuid)
    if 'model_name' not in data:
        raise typer.BadParameter(f"The provided object ID {uuid} did not return any object type. "
                                 f"This UUID is mots likely false")
    resolved_type: str = data['model_name']
    if resolved_type.lower() != expected_type.lower():
        raise typer.BadParameter(f"The provided object ID {uuid} does not point to a {expected_type} but to"
                                 f" a {resolved_type}")
    return resolved_type


@app.command(_CMD_EXPORT_ELN, short_help="Export ELN experiments to a local dir_path",
             help="Export ELN experiments to a local dir_path. Optional filters to (1) restrict the export to "
                  " a unique project_id, (2) a group_name (when you belong to multiple groups), a (3) user and"
                  " (4) expand the export to experiments owned by others (provided you have read access to) "
                  "are available.")
def export_eln_experiments(
        export_dir: str = typer.Option(
            ...,
            "--odir",
            "-o",
            help="Path to where the project_id should be export"
        ),
        project_id: str = typer.Option(
            None,
            "--project",
            "-p",
            help="The UUID of the project_id to restrict the export. "
        ),
        group_name: str = typer.Option(
            None,
            "--group_name",
            "-g",
            help="Export all experiments you can read from the given group_name."
        ),
        username: str = typer.Option(
            None,
            "--username",
            "-u",
            help="Export all experiments you can read of the given username; default user is the stocks user defined in"
                 " the config (which should be you, the command line caller)"
        ),
        include_other_owners: bool = typer.Option(
            False,
            "--all",
            "-a",
            help="If true, experiments owned by others will also be exported. When not set (default); only experiments "
                 "that belong to you or to --username are exported"
        ),
        append: bool = typer.Option(
            False,
            "--resume",
            "-r",
            help="If true and the export dir exists, a diff-like export is perform to"
                 "add/replace new/modified experiments only."
        ),
        conf_file_path: str = typer.Option(
            get_default_config_file_path(),
            "--config-path",
            help="Config file absolute path")
) -> None:
    """
    Export all experiments that belong to a given project_id. The export can be executed in append mode in which case
    only new and modified experiments are exported. The project_id summary page is always freshly rebuilt.

    The following use cases are supported:
    1. export all your own lab notes. In case you belong to multiple groups, you can restrict to a --group_name
    2. export all lab notes about a --project that belong to you (default) or to the --username or --all lab notes
    you can see. The result will be caller-specific as people may have different permissions on the project's lab
    notes.
    Group leaders should be able to export all lab notes of their group_name: this is not supported yet so 'admin'
    should be used for complete project export (with --project & --all options)
    3. export all lab notes from your group_name (GL operation). At the moment this can only be achieved as an 'admin'
    with --group_name & --all
    4. export all notes of a particular user (--username) and optionally restricted to a --group_name or a --project.
    Admin/GL use case (GL not supported yet).
    """
    config_content = get_config(Path(conf_file_path))
    default_url = config_content["default"]
    is_personal_export: bool = False
    export_username: str = config_content[default_url].get("username", getpass.getuser())

    if not include_other_owners and not username:
        # set username to the config's stocks_user; or to the user running the CLI
        username = export_username
        # we'll export notes for the username from all groups (let the permission system apply)
        is_personal_export = True
    if username and export_username == username:
        is_personal_export = True

    if include_other_owners:
        if not group_name or not project_id:
            raise typer.BadParameter(f"--all must be combined with --group_name and/or --project_id")
        # we want to export all for either a group_name or a project. username should not be set ie let it as caller say

    client: StocksClient = StocksClient(config_content)
    stocks_manager: StocksManager = StocksManager(client)

    # check export dir_path
    if Path(export_dir).exists() and not append:
        typer.BadParameter(f"Export directory already exist while --resume is false: {str(export_dir)}")

    Path(export_dir).mkdir(parents=True, exist_ok=True)
    if not Path(export_dir).exists():
        raise typer.BadParameter(f"Failed to create export dir at: {export_dir}")

    if not os.access(str(export_dir), os.W_OK):
        raise typer.BadParameter(f"Cannot write in directory: {str(export_dir)}")

    project = None
    if project_id:
        # Check given id is really a project
        project = stocks_manager.fetch_project(project_id)
        if not project:
            raise typer.BadParameter(f"Wrong value provided for --project, no project found for UUID {project}")
        logging.debug(project.as_simple_json())

    if group_name:
        # validate given group_name
        groups: dict[str, UserGroup] = stocks_manager.list_groups(as_dict=True, keys_lower_case=True)
        if group_name.lower() not in groups:
            for x in groups.values():
                logger.debug(x.name)
            raise typer.BadParameter(f"Wrong value provided for --group_name, no group_name found for  {group_name}")
        else:
            # make sure we have the right case
            group_name = groups[group_name.lower()].name

    # fetch the list of experiments to export
    exps: List[Experiment] = stocks_manager.list_experiments(
        owner=username, group_name=group_name, project_id=project_id, include_deleted=False)
    logger.debug(f"Got {len(exps)} experiments")

    for e in exps:
        logger.debug(e.as_simple_json())
        # each exp gets its own dir named <exp_name>_<id> (<id> to make it unique)
        exp_dir_name = get_experiment_export_dirname(e)
        year_dir_name = str(e.created.year)
        exp_dir: Path = Path(export_dir, year_dir_name, exp_dir_name)
        do_export = True
        if append and exp_dir.exists():
            # this exp was already exported, check if modified date is more recent than the dir create date
            exported: datetime = datetime.fromtimestamp(os.path.getmtime(exp_dir), tz=pytz.UTC)
            last_modified: datetime = e.modified
            do_export = exported < last_modified
            if do_export:
                # remove the whole dir
                shutil.rmtree(exp_dir)

        exp_dir.mkdir(parents=True, exist_ok=True)

        if do_export:
            atts: List[StocksAttachment] = None
            if e.is_frozen:
                # fetch latest .gz
                logging.debug(f"Exporting frozen exp {e.id} : {e.name}")
                atts: List[StocksAttachment] = stocks_manager.list_experiment_archives(
                    experiment_id=e.id, most_recent_only=True)
            else:
                # fetch latest PDF & html
                logging.debug(f"Exporting non-frozen exp {e.id} : {e.name}")
                atts: List[StocksAttachment] = stocks_manager.list_experiment_nightly_backups(
                    experiment_id=e.id, most_recent_only=True)
            # get stuff
            if atts and len(atts) > 0:
                dl_file = requests.get(atts[0].direct_url)
                logging.debug(f"   Downloading {atts[0].name} to {str(exp_dir)}")
                local_path = Path(exp_dir, atts[0].name)
                open(local_path, 'wb').write(dl_file.content)
                # extract
                if atts[0].name.endswith(".zip"):
                    zip_ref = zipfile.ZipFile(local_path)
                    zip_ref.extractall(exp_dir)  # extract file to dir
                    zip_ref.close()

    # dump all exp to csv
    exp_table_path: Path = Path(export_dir, "eln_experiment_list.tsv")
    logging.debug(f"Creating experiment list file in {str(exp_table_path)}")
    id_to_projects: dict = dict()
    with open(exp_table_path, 'w', newline='') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
        writer.writerow(_exp_as_row(e=None, export_dir=export_dir, stocks_server_url=default_url, only_headers=True))
        for e in exps:
            # make sure the Project is set
            if e.project not in id_to_projects:
                id_to_projects[e.project] = stocks_manager.fetch_project(uuid=e.project)
            e.project = id_to_projects[e.project]
            writer.writerow(_exp_as_row(e, export_dir=export_dir, stocks_server_url=default_url))
        tsv_file.close()

    build_static_web_site_for_eln_export(
        dir_path=export_dir, exp_table_path=exp_table_path, export_username=export_username,
        is_personal_export=is_personal_export, exported_project=project,
        exported_group_name=group_name, exported_user=username)


def _determine_output_format(file_path: Path) -> str | None:
    """
    Test output extension and converts it to xlsx (for .xls & .xlsx), csv or json
    :param file_path: a path pointing to a file (does not need to exist)
    :return: xlsx, csv or json or None
    """
    if not file_path:
        return None

    elif file_path.name.lower().endswith(".xls"):
        logger.warning("Notice that the file_path is written as .xlsx. Excel might complain about the extension not "
                       "matching the content.")
        return "xlsx"
    elif file_path.name.lower().endswith(".xlsx"):
        return "xlsx"
    elif file_path.name.lower().endswith((".csv", ".txt")):
        return "csv"
    return "json"


def _find_experiment_file(e: Experiment, experiment_dir_path: Path, extension: str) -> Path | None:
    """
    look for the html or PDF file export for the given experiment
    :param e: the experiment to look for
    :param experiment_dir_path: the dir_path in which the experiment Zip export has been unpacked
    :param extension: html or pdf
    :return:
    """
    if extension != 'pdf' and extension != 'html':
        raise ValueError("extension must be either pdf or html")

    names: List[str] = glob.glob(f"{e.name}*.{extension}", root_dir=experiment_dir_path)
    if not names:
        logger.warning(f"Could not find experiment {extension} file in {str(experiment_dir_path)}")
        return None

    return Path(experiment_dir_path, names[0])  # we r not suppose to have more than one file


def _exp_as_row(e: Optional[Experiment], export_dir: Path | str | None, stocks_server_url: Optional[str],
                only_headers=False) -> List[str]:
    if only_headers:
        return ['UUID', 'Name', 'Project', 'Owner', 'Group', 'Completion Status',
                'Is Frozen', 'Summary', 'Started', 'Completed', 'Last Modified', 'Last Modified By',
                'Frozen', 'HTML', 'PDF', 'Experiment Live Link', 'Project Live Link']
    if stocks_server_url[-1] != "/":
        stocks_server_url = stocks_server_url + "/"

    exp_dir_name = get_experiment_export_dirname(e)
    year_dir_name = str(e.created.year)
    experiment_dir_path = Path(export_dir, year_dir_name, exp_dir_name)

    # get the html exp file name
    html_exp_rel_path: Path | None = _find_experiment_file(e, experiment_dir_path, "html")
    # get the pdf exp file name
    pdf_exp_rel_path: Path | None = _find_experiment_file(e, experiment_dir_path, "pdf")

    link_to_stocks_exp: str = stocks_server_url + e.id
    link_to_stocks_project: str = stocks_server_url + (e.project.id if isinstance(e.project, Project) else e.project)

    return [e.id, e.name, e.project.name, e.owner, e.owned_by,
            e.status.value, str(e.is_frozen), e.summary if e.summary else "",
            e.start_date.strftime('%Y-%m-%d') if e.start_date else "",
            e.completed_date.strftime('%Y-%m-%d') if e.completed_date else "",
            e.modified.strftime('%Y-%m-%d') if e.modified else "",
            e.modified_by,
            e.freeze_date.strftime('%Y-%m-%d') if e.freeze_date else "",
            html_exp_rel_path.as_uri() if html_exp_rel_path else "",
            pdf_exp_rel_path.as_uri() if pdf_exp_rel_path else "",
            link_to_stocks_exp, link_to_stocks_project]


def make_clickable_experiment(url_html, url_pdf, url_stocks):
    if not url_html and not url_pdf and not url_stocks:
        return ""
    s = "["
    if url_html:
        s = s + '<a href="{}" rel="noopener noreferrer" target="_blank">HTML</a>'.format(url_html)

    if url_pdf:
        if s != "[":
            s = s + '|'
        s = s + '<a href="{}" rel="noopener noreferrer" target="_blank">PDF</a>'.format(url_pdf)

    if url_stocks:
        if s != "[":
            s = s + '|'
        s = s + '<a href="{}" rel="noopener noreferrer" target="_blank">STOCKS</a>'.format(url_stocks)

    s = s + "]"
    return s


def make_clickable_project(name, url_stocks):
    if not url_stocks:
        return name

    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url_stocks, name)


def _find_experiment_file(e: Experiment, experiment_dir_path: Path, extension: str) -> Path | None:
    """
    look for the html or PDF file export for the given experiment
    :param e: the experiment to look for
    :param experiment_dir_path: the dir in which the experiment Zip export has been unpacked
    :param extension: html or pdf
    :return:
    """
    if extension != 'pdf' and extension != 'html':
        raise ValueError("extension must be either pdf or html")

    names: List[str] = glob.glob(f"{e.name}*.{extension}", root_dir=experiment_dir_path)
    if not names:
        logger.warning(f"Could not find experiment {extension} file in {str(experiment_dir_path)}")
        return None

    return Path(experiment_dir_path, names[0])  # we r not suppose to have more than one file


def determine_output_format(output):
    if not output.name.endswith((".xls", ".xlsx", ".csv", ".txt")):
        return "json"
    elif output.name.endswith(".xls"):
        logger.warning("Notice that the output is written as .xlsx. Excel might complain about the extension not "
                       "matching the content.")
    elif output.name.endswith((".csv", ".txt")):
        return "csv"
    return "xlsx"


def get_query_params(query_params: Optional[List[str]]) -> Dict[str, Any]:
    """
    :param query_params: a list of key=value strings
    :return:
    """
    _query_params: Dict[str, Any] = {"response_format": "flat"}
    if query_params:
        for param in query_params:
            k, v = param.split("=")
            _query_params[k] = v
    return _query_params


def create_magefile(outpath: Path, table: pd.DataFrame, study: Study, assay_dict: Dict[str, Assay], sdrf: pd.DataFrame,
                    is_idf: bool = True, is_sdrf: bool = True, stocks_comments: bool = True) \
        -> None:
    """
    Writes a CSV file formated with the MAGE-TAB specifications.
    :param outpath: Path where the cvs is written
    :param table: metadata table from stocks
    :param study: model.Study object
    :param assay_dict: Dictionary containing information relating to the assays of the study
    :param sdrf: pandas.DataFrame of the SDRF part of the magetab
    :param is_idf: True to include IDF in the MAGE-TAB.
    :param is_sdrf: True to include SDRF in the MAGE-TAB
    :param stocks_comments: True to include stocks related information as comment in the MAGE-TAB
    """
    if is_idf:
        f = open(outpath, "a")
        f.write('[IDF]\n')
        f.write(f'Investigation Title\t"{study.name}"\n')
        f.write(f'Experiment Description\t"{study.description}"\n')
        f.write("Comment[AEExperiment]\t\n")
        if stocks_comments:
            f.write(f'"{COMMENT_STOCKS_UUID}"\t"{study.id}"\n')
        f.close()
        IDF_study: pd.DataFrame = create_idf_design(study)
        IDF_study.to_csv(outpath, mode="a", header=False, index=False, sep="\t")
        IDF_exp_fac: pd.DataFrame = create_idf_experimental_factors(study.experimental_factors)
        IDF_users: pd.DataFrame = create_idf_users(study)
        IDF_protocol: pd.DataFrame = create_idf_protocol(study.protocols, study.assays)
        if not stocks_comments:
            IDF_protocol.drop(index=IDF_protocol.iloc[-1].name, inplace=True)

        if len(IDF_exp_fac.columns) == 1:
            logger.warning("IDF experimental factors table is empty")
        write_df_in(outpath, IDF_exp_fac)
        if len(IDF_users.columns) == 1:
            logger.warning("IDF users table is empty")
        write_df_in(outpath, IDF_users)
        f = open(outpath, "a")
        f.write(f'Public Release Date\t{MAGETAB_RELEASE_DATE}\n\n')
        f.close()
        if len(IDF_protocol.columns) == 1:
            logger.warning("IDF protocol table is empty")
        write_df_in(outpath, IDF_protocol)

        f = open(outpath, "a")
        f.write('Term Source Name\tMGED Ontology\tArrayExpress\tEFO\n')
        f.write('Term Source File\thttp://mged.sourceforge.net/ontologies/MGEDontology.php\t'
                'https://www.ebi.ac.uk/biostudies/arrayexpress\thttp://www.ebi.ac.uk/efo/\n\n')
        f.close()

    if is_sdrf:
        f = open(outpath, "a")
        f.write('[SDRF]\n')
        f.close()
        sdrf.to_csv(outpath, mode="a", header=True, index=False, sep="\t")


def create_sdrf(df: pd.DataFrame, study: Study, assay_dict: Dict[str, SequencingAssay],
                annotations_dict: Dict[str, dict[str, AnnotationType | None | list[str] | bool]],
                stocks_comments: bool = True) -> pd.DataFrame:
    """
    Create the dataframe with all information of the SDRF
    """
    single_cell_bool, has_spike_ins = check_table_bools(df)
    # Extract experimental factors
    annotation_df, factors_df = create_annofactor_df(annotations_dict)
    new_df = pd.DataFrame()
    if study.assays[0].technology == Technology.SEQUENCING:
        new_df["Source Name"] = df["Sample"]
        if stocks_comments:
            new_df['Comment[Sample_stocks_id]'] = df["Sample ID"]
        new_df["Material Type"] = TODO
        new_df["Term Source REF"] = TERM_SOURCE_REF
        new_df = pd.concat([new_df, pd.DataFrame(annotation_df)], axis=1)

        protocol_type_df: pd.DataFrame = create_protocol_ref(df, study.protocols)
        new_df = pd.concat([new_df, protocol_type_df], axis=1)

        new_df["Extract Name"] = df["Sample"]
        new_df["temp"] = df["Material Type"]
        new_df.rename(columns={'temp': 'Material Type'}, inplace=True)
        new_df["Term Source REF 2"] = TERM_SOURCE_REF
        if stocks_comments:
            new_df['Comment[Dataset_stocks_id]'] = df["Dataset ID"]
        new_df["Comment[BARCODE]"] = df["Barcode"]
        new_df['Comment[LIBRARY_LAYOUT]'] = df['Assay ID'].apply(lambda x: runtype_layout_map[assay_dict[x].runtype])
        new_df['Comment[LIBRARY_SOURCE]'] = df['Library Source']
        new_df['Comment[LIBRARY_STRATEGY]'] = df['Library Strategy']
        new_df['Comment[LIBRARY_SELECTION]'] = df['Library Selection']
        new_df['Comment[QUALITY_SCORING_SYSTEM]'] = QUALITY_SCORING_SYSTEM
        new_df['Comment[LIBRARY_ENCODING]'] = LIBRARY_ENCODING
        new_df['Comment[ASCII_OFFSET]'] = ASCII_OFFSET
        if runtype_layout_map[SequencingRunType.PAIRED_END] in new_df['Comment[LIBRARY_LAYOUT]'].unique():
            new_df['Comment[ORIENTATION]'] = df['Library Orientation']
        if single_cell_bool:
            new_df["Comment[Library Construction]"] = df["Single Cell Library Construction"].apply(
                lambda x: stocks_annotare_library_contruction_map.get(x, x))
            single_cell_df = new_df["Comment[Library Construction]"].apply(
                lambda x: ','.join(single_cell_annotare_fillin(x))).str.split(",", expand=True)
            single_cell_df.columns = [f"Comment[{x}]" for x in MAGETAB_HEADER_SINGLE_CELL_ANNOTARE]
            new_df = pd.concat([new_df, single_cell_df], axis=1)
            new_df["Comment[Single Cell Isolation]"] = merge_df_columns(new_df["Comment[Single Cell Isolation]"],
                                                                        df["Single Cell Isolation"])
            new_df["Comment[End Bias]"] = merge_df_columns(new_df["Comment[End Bias]"], df["Library End Bias"])
            new_df["Comment[Primer]"] = merge_df_columns(new_df["Comment[Primer]"], df["RT Primer Type"])
            if has_spike_ins:
                new_df["Comment[Spike In]"] = merge_df_columns(new_df["Comment[Spike In]"], df["Kit name"])
                new_df["Comment[Spike in dilution]"] = merge_df_columns(new_df["Comment[Spike in dilution]"],
                                                                        df["Kit dilution"])
            else:
                new_df.drop(columns=["Comment[Spike In]", "Comment[Spike in dilution]"], inplace=True)
        elif has_spike_ins:
            new_df["Comment[Spike In]"] = df["Kit name"]
            new_df["Comment[Spike in dilution]"] = df["Kit dilution"]

        new_df["temp"] = df['Assay ID'].apply(
            lambda
                x: f'Standard {assay_dict[x].instrumentrun.instrument.model} {assay_dict[x].runtype.value} Sequencing')
        new_df.rename(columns={'temp': 'Protocol REF'}, inplace=True)

        new_df["Performer"] = df['Assay ID'].apply(lambda x: owner_name(assay_dict[x]))
        new_df["Assay Name"] = df["Assay Name"]
        if stocks_comments:
            new_df['Comment[Assay_stocks_id]'] = df["Assay ID"]
        new_df["Technology Type"] = df['Assay ID'].apply(lambda x: assay_dict[x].technology.value + ' assay')
        new_df["Array Data File"] = df["File Name"]

        new_df["Comment[MD5]"] = df["Checksum"]
        new_df["Comment[BARCODE]"] = df["Barcode"]

        new_df = pd.concat([new_df, pd.DataFrame(factors_df)], axis=1)
    return new_df


def ena_submission(export_dir: str, study_id: str, ena_file_outpath: Dict[str, str], ena_cred_path: str,
                   to_del_credentials: bool, execute: bool, stocks_manager: StocksManager) -> None:
    cmd = f"cd {export_dir}; ena-upload-cli --action add --secret {ena_cred_path} --center embl"
    for name, p in ena_file_outpath.items():
        cmd = f"{cmd} --{name} {p}"
    if not execute:
        cmd = f"{cmd} --dev"
        # Create fake data if needed
        FAKE_DIR = None
        if ena_file_outpath.get('run'):
            FAKE_DIR = os.path.join(export_dir, 'fake_data')
            while os.path.exists(FAKE_DIR):  # Making sure an already existing folder will not be deleted.
                FAKE_DIR = FAKE_DIR + '_tmp'
            create_fake_data(FAKE_DIR, pd.read_table(ena_file_outpath['run']))
            cmd = f"{cmd} --data {os.path.join(FAKE_DIR, '*')}"
        else:
            cmd = f"{cmd} --no_data_upload"
        # Call ena-upload-cli command with fake data in ENA test sandbox
        _ena_upload_cli(cmd, to_del_credentials, ena_cred_path, FAKE_DIR)

    else:
        # Call ena-upload-cli command for metadata submission to the ENA
        _ena_upload_cli(cmd, to_del_credentials, ena_cred_path)

    for name, f in ena_file_outpath.items():  # Replace old tables with updated ones
        os.remove(f)
        file_name = f.split('.')
        os.rename(f"{file_name[0]}_updated.tsv", f"{file_name[0]}.tsv")

    if execute:
        # upload accession to STOCKS
        timestamp = datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
        receipt_path = os.path.join(export_dir, f"receipt_{timestamp}.xml")
        os.rename(os.path.join(export_dir, 'receipt.xml'), receipt_path)
        done = upload_accessions(receipt_path, stocks_manager, study_id)
        if done:
            logger.info(f"All done")


def upload_accessions(receipt_path: str, stocks_manager: StocksManager, study_id: str | None) -> bool:
    """
    Parse an XML file and uploads accession numbers into STOCKS
    :param receipt_path: Path of XML file
    :param study_id: UUID of the study
    :param stocks_manager: stocksapi.StocksManager
    :raises ValueError: No study id is found or both provided dont match
    """
    accession_dicts = parse_receipt(receipt_path)
    # Check ids
    receipt_study_id = list(accession_dicts[0].keys())
    if receipt_study_id:
        receipt_study_id = receipt_study_id[0]
    if not receipt_study_id and not study_id:
        raise ValueError(f"No study ids was provided nor found in the receipt file")
    if receipt_study_id and study_id and receipt_study_id != study_id:
        raise ValueError(f"The provided study id doesnt match the receipt study id")
    study_id = study_id if study_id else receipt_study_id

    done = upload_ena_annotation(accession_dicts, stocks_manager)
    if done:
        stocks_manager.upload_attachment(receipt_path, study_id, ModelType.STUDY)
    return done
