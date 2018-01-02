#!/bin/bash -xe

pre-commit run -a
pylint \
    --rcfile=pylintrc \
    --disable=duplicate-code \
    ArchiveInterfaceServer.py \
    archiveinterface \
    archiveinterface.archive_interface \
    archiveinterface.archive_interface_responses \
    archiveinterface.archive_interface_error \
    archiveinterface.archive_utils \
    archiveinterface.id2filename \
    archiveinterface.archivebackends.archive_backend_factory \
    archiveinterface.archivebackends.abstract.abstract_backend_archive \
    archiveinterface.archivebackends.abstract.abstract_status \
    archiveinterface.archivebackends.posix.posix_backend_archive \
    archiveinterface.archivebackends.posix.posix_status \
    archiveinterface.archivebackends.posix.extendedfile \
    archiveinterface.archivebackends.hpss.hpss_backend_archive \
    archiveinterface.archivebackends.hpss.hpss_extended \
    archiveinterface.archivebackends.hpss.hpss_status \
    archiveinterface.archivebackends.oracle_hms_sideband.extended_hms_sideband \
    archiveinterface.archivebackends.oracle_hms_sideband.hms_sideband_backend_archive \
    archiveinterface.archivebackends.oracle_hms_sideband.hms_sideband_status \
    archiveinterface.archivebackends.oracle_hms_sideband.hms_sideband_orm \
    post_deployment_tests/deployment_test.py
