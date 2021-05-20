import os
import pytest

from espresso.siteconfig import SiteConfig


def test_pbs_exceptions(tmpdir):
    "check if an exception is raised when `scratchenv` variable is undefined"

    tmpdir.chdir()
    pytest.raises(OSError, SiteConfig, "PBS", scratchenv="MYSCRATCH0000")


def test_slurm_exceptions(tmpdir):
    "check if an exception is raised when `scratchenv` variable is undefined"

    tmpdir.chdir()
    pytest.raises(OSError, SiteConfig, "SLURM", scratchenv="MYSCRATCH0000")


def test_pbs_variables(tmpdir):

    tmpdir.chdir()

    os.environ["SCRATCH"] = str(tmpdir)
    os.environ["PBS_JOBID"] = "12345678"
    os.environ["PBS_O_WORKDIR"] = str(tmpdir)
    nodefile = tmpdir.join("nodefile")
    os.environ["PBS_NODEFILE"] = str(nodefile)

    # create nodefile for 2 nodes with 16 cpu each
    nodes = ["node-{0:d}".format(i) for i in range(2) for _ in range(16)]
    with nodefile.open("w") as nf:
        for name in nodes:
            nf.write(name + "\n")

    site = SiteConfig("PBS")

    assert site.jobid == "12345678"
    assert site.submitdir == str(tmpdir)
    assert site.nprocs == 32
    assert site.hosts == nodes
    assert site.global_scratch == str(tmpdir)

    site.__class__._Singleton__erase()


def test_slurm_variables(tmpdir):

    tmpdir.chdir()

    os.environ["SCRATCH"] = str(tmpdir)
    os.environ["SLURM_JOB_ID"] = "87654321"
    os.environ["SUBMITDIR"] = str(tmpdir)
    os.environ["SLURM_JOB_NUM_NODES"] = "2"
    os.environ["SLURM_TASKS_PER_NODE"] = "12"
    os.environ["SLURM_JOB_NODELIST"] = "node-0,node-1"

    site = SiteConfig("SLURM")

    assert site.jobid == "87654321"
    assert site.submitdir == str(tmpdir)
    assert site.nprocs == 24
    assert site.global_scratch == str(tmpdir)

    site.__class__._Singleton__erase()
