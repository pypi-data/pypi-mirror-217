import logging
import os
from pathlib import Path
import sys
from typing import Dict, Optional

from . import utils, core, codechat

# Get access to logger
log = logging.getLogger("ptxlogger")


def html(
    ptxfile: Path,
    pub_file: Path,
    output: Path,
    stringparams: Dict[str, str],
    custom_xsl: Optional[Path],
    xmlid_root: Optional[str],
    zipped: bool = False,
) -> None:
    os.makedirs(output, exist_ok=True)
    log.info(f"\nNow building HTML into {output}\n")
    if xmlid_root is not None:
        log.info(f"Only building @xml:id `{xmlid_root}`\n")
    if zipped:
        file_format = "zip"
    else:
        file_format = "html"
    # ensure working directory is preserved
    with utils.working_directory(Path()):
        try:
            core.html(
                ptxfile,
                pub_file.as_posix(),
                stringparams,
                xmlid_root,
                file_format,
                custom_xsl and custom_xsl.as_posix(),  # pass None or posix string
                None,
                output.as_posix(),
            )
            pp = utils.project_path(ptxfile)
            assert pp is not None, f"Invalid project path to {ptxfile}."
            codechat.map_path_to_xml_id(ptxfile, pp, output.as_posix())
        except Exception as e:
            log.critical(e)
            log.debug("Exception info:\n##################\n", exc_info=True)
            log.info("##################")
            sys.exit("Failed to build html.  Exiting...")


def latex(
    ptxfile: Path,
    pub_file: Path,
    output: Path,
    stringparams: Dict[str, str],
    custom_xsl: Optional[Path],
) -> None:
    os.makedirs(output, exist_ok=True)
    log.info(f"\nNow building LaTeX into {output}\n")
    # ensure working directory is preserved
    with utils.working_directory(Path()):
        try:
            core.latex(
                ptxfile,
                pub_file.as_posix(),
                stringparams,
                custom_xsl and custom_xsl.as_posix(),  # pass None or posix string
                None,
                output.as_posix(),
            )
        except Exception as e:
            log.critical(e)
            log.debug("Exception info:\n##################\n", exc_info=True)
            log.info("##################")
            sys.exit("Failed to build latex.  Exiting...")


def pdf(
    ptxfile: Path,
    pub_file: Path,
    output: Path,
    stringparams: Dict[str, str],
    custom_xsl: Optional[Path],
    pdf_method: str,
) -> None:
    os.makedirs(output, exist_ok=True)
    log.info(f"\nNow building LaTeX into {output}\n")
    # ensure working directory is preserved
    with utils.working_directory(Path()):
        try:
            core.pdf(
                ptxfile,
                pub_file.as_posix(),
                stringparams,
                custom_xsl and custom_xsl.as_posix(),  # pass None or posix string
                None,
                dest_dir=output.as_posix(),
                method=pdf_method,
            )
        except Exception as e:
            log.critical(e)
            log.debug("Exception info:\n##################\n", exc_info=True)
            log.info("##################")
            sys.exit("Failed to build pdf.  Exiting...")


def custom(
    ptxfile: Path,
    pub_file: Path,
    output: Path,
    stringparams: Dict[str, str],
    custom_xsl: Path,
    output_filename: Optional[str] = None,
) -> None:
    os.makedirs(output, exist_ok=True)
    if output_filename is not None:
        output_filepath = output / output_filename
        output_dir = None
        log.info(f"\nNow building with custom {custom_xsl} into {output_filepath}\n")
    else:
        output_filepath = None
        output_dir = output
        log.info(f"\nNow building with custom {custom_xsl} into {output}\n")
    # ensure working directory is preserved
    with utils.working_directory(Path()):
        try:
            core.xsltproc(
                custom_xsl,
                ptxfile,
                output_filepath,
                output_dir=output_dir,
                stringparams=stringparams,
            )
        except Exception as e:
            log.critical(e)
            log.debug("Exception info:\n##################\n", exc_info=True)
            log.info("##################")
            sys.exit("Failed custom build.  Exiting...")


# build (non Kindle) ePub:
def epub(
    ptxfile: Path, pub_file: Path, output: Path, stringparams: Dict[str, str]
) -> None:
    os.makedirs(output, exist_ok=True)
    try:
        utils.npm_install()
    except Exception as e:
        log.debug(e)
        sys.exit(
            "Unable to build epub because node packages are not installed.  Exiting..."
        )
    log.info(f"\nNow building ePub into {output}\n")
    with utils.working_directory(Path()):
        try:
            core.epub(
                ptxfile,
                pub_file.as_posix(),
                out_file=None,  # will be derived from source
                dest_dir=output.as_posix(),
                math_format="svg",
                stringparams=stringparams,
            )
        except Exception as e:
            log.critical(e)
            log.debug("Exception info:\n##################\n", exc_info=True)
            log.info("##################")
            sys.exit("Failed to build epub.  Exiting...")


# build Kindle ePub:
def kindle(
    ptxfile: Path, pub_file: Path, output: Path, stringparams: Dict[str, str]
) -> None:
    os.makedirs(output, exist_ok=True)
    try:
        utils.npm_install()
    except Exception as e:
        log.critical(e)
        sys.exit(
            "Unable to build Kindle ePub because node packages are not installed.  Exiting..."
        )
    log.info(f"\nNow building Kindle ePub into {output}\n")
    with utils.working_directory(Path()):
        try:
            core.epub(
                ptxfile,
                pub_file.as_posix(),
                out_file=None,  # will be derived from source
                dest_dir=output.as_posix(),
                math_format="kindle",
                stringparams=stringparams,
            )
        except Exception as e:
            log.critical(e)
            log.debug("Exception info:\n##################\n", exc_info=True)
            log.info("##################")
            sys.exit("Failed to build kindle ebook.  Exiting...")


# build Braille:
def braille(
    ptxfile: Path,
    pub_file: Path,
    output: Path,
    stringparams: Dict[str, str],
    page_format: str = "emboss",
) -> None:
    os.makedirs(output, exist_ok=True)
    log.warning(
        "Braille output is still experimental, and requires additional libraries from liblouis (specifically the file2brl software)."
    )
    try:
        utils.npm_install()
    except Exception as e:
        log.debug(e)
        sys.exit(
            "Unable to build braille because node packages could not be installed.  Exiting..."
        )
    log.info(f"\nNow building braille into {output}\n")
    with utils.working_directory(Path()):
        try:
            core.braille(
                xml_source=ptxfile,
                pub_file=pub_file.as_posix(),
                out_file=None,  # will be derived from source
                dest_dir=output.as_posix(),
                page_format=page_format,  # could be "eboss" or "electronic"
                stringparams=stringparams,
            )
        except Exception as e:
            log.critical(e)
            log.debug("Exception info:\n##################\n", exc_info=True)
            log.info("##################")
            sys.exit("Failed to build braille.  Exiting...")


# Build WeBWorK sets (for archive)
def webwork_sets(
    ptxfile: Path,
    pub_file: Path,
    output: Path,
    stringparams: Dict[str, str],
    zipped: bool = False,
) -> None:
    os.makedirs(output, exist_ok=True)
    log.info(f"\nNow building WeBWorK Sets into {output}\n")
    # ensure working directory is preserved
    with utils.working_directory(Path()):
        try:
            core.webwork_sets(
                xml_source=ptxfile,
                pub_file=pub_file.as_posix(),
                stringparams=stringparams,
                dest_dir=output.as_posix(),
                tgz=zipped,
            )
        except Exception as e:
            log.critical(e)
            log.debug("Exception info:\n##################\n", exc_info=True)
            log.info("##################")
            sys.exit("Failed to build html.  Exiting...")
