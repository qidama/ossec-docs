from paver.easy import *
import paver.doctools


import sys
sys.path.append("./")


options(
    tests=Bunch(
        tdir="./tests/",
    ),
    sphinx=Bunch(
        builddir="_build",
        sourcedir="."
    ),
    ossec=Bunch(
        base="/var/ossec",
        version="2.4.1",
    )
)

@task 
def auto():
    """Auto load the ossec config if installed and readable"""
    p = path("/etc/ossec-init.conf")
    try:
        data = p.open().read()
    except IOError:
        return 

@task 
@cmdopts([("xunit", 'x', 'Create XUnit output files')])
def tests():
    """Run all tests on all rules that have them"""
    if options.xunit:
        sh("nosetests --with-xunit or_utils.runtests")
    else:
        sh("nosetests or_utils.runtests")



@task 
def rules2rst():
    """Convert all rules in to rst pages to act as documations"""
    from or_utils import rules2rst 
    pass

@task
@needs('paver.doctools.html')
@needs('rules2rst')
def html():
    """Generate Publishable HTML docs using sphinx"""
    builtdocs = path("docs") / options.sphinx.builddir / "html"
    destdir = path("docs") / "docs"
    destdir.rmtree()
    builtdocs.move(destdir)