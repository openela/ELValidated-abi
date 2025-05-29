
# Table of Contents

1.  [A tool for checking an RPM packages](#elverify-abi)
2.  [A tool for submitting an ABI XML to a git repo](#abirepo)

# A git repository for archiving RPM ABI XMLs

The repository structure is as follows:

    <package_name> -> <Vendor> -> <Architecture> -> XML files

where:

-   package_name is an rpm package name (e.g., glibc)
-   Vendor is the vendor name who prepared the RPM package (e.g., Oracle)
-   Architecture is the architecure for which the RPM package is for (e.g., x86_64)
-   The DSO XML file contains the abi corpus group for all public DSOs
    found in an RPM package. The public DSOs are found using package's
    provide information (i.e., rpm -qp --provides). These files are
    named using the following pattern:
    {PAK_NAME}-{VERSION}-{RELEASE}.xml.

Example:

```text
    GitDir
    └── glibc
        ├── Oracle
        │   └── x86_64
        │       ├── glibc-2.34-100.0.1.el9_4.4.xml
        │       ├── glibc-2.34-125.0.1.el9_5.1.xml
        │       ├── glibc-2.34-28.0.1.el9_0.xml
        └── Rocky
            └── x86_64
                ├── glibc-2.34-100.el9_4.4.xml
```

<a id="dsitrocompat"></a>
# A tool for checking distro RPM packages

## elverify-abi

elverify-abi is a script built around libabigail tools that
quickly checks either if a RPM is compatible against a Vendor distro.

### Comparing rpm Vs XML DB folder

- It assumes the XML DB folder is located one level up from invocation
 point of the tool, namely "../gitxml". This value can be overwritten
 by using --dir <newFolder> option
- The debuginfo package name is not required as long as it is located
 along rpm package and respects the debuginfo naming scheme.
- It only does a real comparison if the versions are identical. If
 they are not it return a negative result immediately.

Example: Compare against a Rocky RPM

$elverify-abi glibc-2.34-100.el9_4.4.x86_64.rpm
Compatible

Observations: The elverify-abi tool will employ first the Vendor
 selection, namely, it searches for a Rocky version of glibc, and, if
 it is not found, a default one (in our exercise is Oracle) is chosen.
 Next, the tool will employ a heuristic to match the closest
 version-release tuple in the ABI XML DB. Thus, the diff is done
 against glibc/Oracle/x86_64/glibc-2.34-100.0.1.el9_4.4.xml file.

### Returning Values

elverify-abi returns the next values

| Mnemonic | Value | Meaning |
|----------|-------|---------|
| COMPATIBLE | 0 | The analysis is successful, the package(s) are compatible |
| NOTCOMPATILBE| 256 | The package(s) are not compatible |
| EINVAL | 22 | Versions must match |
| EEXIST | 17 | An error is detected while accessing ABI XML DB |
| EOTHER  | 1  | An internal error is detected |

<a id="abirepo"></a>

# A tool for submitting an ABI XML to a git repo

A RPM containing public DSOs can be processed into ABI XML. This
 ABIXML is then checked against a given git repo, and if it is new or
 different it is submitted to the git repo.

## ABIREPO

ABIREPO is a wrapper on the libabigail tools to generate ABIXML
documents for a given RPM package. It archives the RPM's ABI XML
documents in a git repository.

### Usage

abirepo [-h] [--loglevel {info,warning,error,debug,critical}] --git GIT [--branch BRANCH]
        [--abidw ABIDW] [--d1 D1]
        RPM1

Where

-   -h Shows a help message and exit
-   --loglevel Sets the logging level, default is set to INFO, but one
    can set it to DEBUG, WARNING, ERROR and CRITICAL. This option is optional.
-   --git The Git working tree. This option is required.
-   --branch The branch used from Git Repo. This option is optional.
-   --abidw Path to abidw program (optional).
-   --d1 Optional debug package needed by the processed RPM.
-   RPM1 Required RPM package.

### Returning Values

| Mnemonic | Value | Meaning |
|----------|-------|---------|
| OK | 0 | The RPM file is successfully processed |
| EOTHER  | 1  | An internal error is detected |

## Examples

Prerequisites:

-   A git repository; if none, then ithe user must create a
    directory (mkdir gitTest), and initialize a git repo in
    this newly created folder (git init).
-   One or more RPM file and their associated debuginfo packages.
-   libabigail v2.5+ installed in the path.

### Submitting an RPM file to Git repo

Submmitting an RPM is the basic operation that populates an ABI XML git repo.

For this operation, we use:

    abirepo --git gitTest glibc-2.34-100.el9_4.4.x86_64.rpm

In the example above, the abirepo script is decompressing both
the glibc rpm package and its debuginfo package into a temporary
folder. Then libabigail's 'abidw' tool is run on the provided DSOs.
The resulted abixml files are commited to the given git repository.

