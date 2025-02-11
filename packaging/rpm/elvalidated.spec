Name:           elvalidated-abi
Version:        0.99
Release:        1%{?dist}
Summary:        OpenELA tool to verify ABI compatibility
BuildArch:      noarch
License:        Apache-2.0 WITH LLVM-exception and GPLv2 and MIT and BSD-3-Clause and BSD
URL:            https://github.com/openela/elvalidated-abi
Source0:	%{name}-%{version}.tar.gz
Source1:	https://files.pythonhosted.org/packages/bf/d4/26f5c9835d4d648e4f22b5fb91288457698e928aaf9d4ab7eff405b7ef03/libarchive-0.4.7.tar.gz
Source2:	https://files.pythonhosted.org/packages/c0/89/37df0b71473153574a5cdef8f242de422a0f5d26d7a9e231e6f169b4ad14/gitpython-3.1.44.tar.gz
Source3:	https://files.pythonhosted.org/packages/5b/1e/ccb1b2f1cc9f3d5351bf0ab9db4db30ca349f7d3b23b2751e4e2fb48e50f/rpmfile-2.1.0.tar.gz
Source4:	https://files.pythonhosted.org/packages/72/94/63b0fc47eb32792c7ba1fe1b694daec9a63620db1e313033d18140c2320a/gitdb-4.0.12.tar.gz
Source5:	https://files.pythonhosted.org/packages/44/cd/a040c4b3119bbe532e5b0732286f805445375489fceaec1f48306068ee3b/smmap-5.0.2.tar.gz

Patch0:		0001-Provide-built-in-deps-by-modifying-python-script.patch

BuildRequires:  python3
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools_scm
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  python-rpm-macros python3-rpm-macros python-srpm-macros

Requires:       python3
Requires:       rpm
Requires:       cpio
#libabigail requires patches to enable CTF backend
Requires:       libabigail >= 2.6-1
Requires:       git

%description
Collection of tools to generate reference XML files containing ABI data for submitted rpm packages, 
to upload them to a git repo, and to run comparisons of packages and data against each other.

%prep
%autosetup


%build
#populate dirs for python deps
mkdir -p elvalidated
tar -zxvf %SOURCE1 --directory=elvalidated
tar -zxvf %SOURCE2 --directory=elvalidated
tar -zxvf %SOURCE3 --directory=elvalidated
tar -zxvf %SOURCE4 --directory=elvalidated
tar -zxvf %SOURCE5 --directory=elvalidated

mkdir -p site3_packages
bundled="libarchive gitpython rpmfile gitdb smmap"
for pkg in $bundled; do
pushd elvalidated/${pkg}*
%{__python3} setup.py install -O1 --prefix=%{_prefix} --root=../../site3_packages
popd
done

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{python3_sitelib}/elvalidated/
mkdir -p %{buildroot}%{_bindir}
%{__cp} -ar elvalidated %{buildroot}%{python3_sitelib}/
%{__install} -pD -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
%{__install} -pD -m 0755 elvalidated-abirepo %{buildroot}%{_bindir}/elvalidated-abirepo
mv %{_builddir}/%{name}-%{version}/site3_packages/usr/*/*/site-packages/* %{buildroot}%{python3_sitelib}/elvalidated/
#fix shebang
sed -i -e 's|\/usr\/bin\/env\ python|\/usr\/bin\/env\ python3|g' %{buildroot}%{python3_sitelib}/elvalidated/gitpython-3.1.44/setup.py
sed -i -e 's|\/usr\/bin\/env\ python|\/usr\/bin\/env\ python3|g' %{buildroot}%{python3_sitelib}/elvalidated/smmap-5.0.2/setup.py

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}
%{_bindir}/elvalidated-abirepo
%{python3_sitelib}/elvalidated


%changelog
* Tue Jun 10 2025 Alex Burmashev <alexander.burmashev@oracle.com> - 0.99-1
- init
