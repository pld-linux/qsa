#
# Fuck Trolltech
%define 	_noautocompressdoc 	*.xml
Summary:	Qt Script for Applications
Summary(pl): 	System skryptowania Qt
Name:		qsa
Version:	1.1.0
Release:	1
License:	GPL
Group:		X11/Libraries
Source0:	ftp://ftp.trolltech.com/qsa/source/%{name}-x11-free-%{version}.tar.gz
# Source0-md5:	7394ebb3cf1c2576d61f8eaff9773b25
Patch0:		%{name}-buildsystem.patch
URL:		http://www.trolltech.com/products/qsa/index.html
BuildRequires:	qt-devel >= 3.1.1-4
BuildRequires:	sed >= 4.0
Requires:	qt >= 3.1.1-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt Script for Applications.

%description -l pl
System skryptowania Qt.

%package libs
Summary:	QSA - libraries
Summary(pl):	QSA - biblioteki
Group:		X11/Libraries
Requires(post,preun):	qt-utils
Requires:       qt >= 3.2-0.030405.4

%description libs
Qt Script for Applications - libraries.

%description libs -l pl
System skryptowania Qt - biblioteki.

%package devel
Summary:        QSA - headers for libraries
Summary(pl):    QSA - pliki nag³ówkowe dla bibliotek
Group:          X11/Libraries
Requires: 	qsa-libs = %{version}
Requires:       qt-devel >= 3.2-0.030405.4

%description devel
Qt Script for Applications - headers for libraries.

%description devel -l pl
System skryptowania Qt - pliki nag³ówkowe dla bibliotek.

%package examples
Summary:        QSA - examples for developers
Summary(pl):    QSA - przyk³adowe programy dla programistów
Group:          X11/Libraries

%description examples
Qt Script for Applications - examples for developers.

%description examples -l pl
System skryptowania Qt - przyk³adowe programy dla programistów.

%package -n qt-plugin-qsa-quickide
Summary:        QSA - no idea what this is.
Group:          X11/Libraries
Requires:       qsa-libs = %{version}

%description -n qt-plugin-qsa-quickide
Qt Script for Applications - ?.

%package -n qt-plugin-qsa-quickcustom
Summary:        QSA - no idea what this is.
Group:          X11/Libraries
Requires:       qsa-libs = %{version}

%description -n qt-plugin-qsa-quickcustom
Qt Script for Applications - ?.

%prep
%setup -q -n %{name}-x11-free-%{version}
%patch0 -p1 -b .x

%build
# Fuck trolltechs build system ideas
export QTDIR=%{_usr}
export QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++/
export LD_LIBRARY_PATH="`/bin/pwd`/src/qsa:$LD_LIBRARY_PATH"

find . -name Makefile -exec rm {} \;


export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcflags}"
CONF="CONFIG+=thread"
cd src/qsa
cat >> qsconfig.h << EOF
#ifndef QS_CONFIG_H
#define QS_CONFIG_H
/* Trolltech sucks */
#endif

EOF
cd ../
qmake "${CONF}" 
%{__make} 

%install
rm -rf  $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_datadir}/qt/mkspecs/linux-g++,%{_includedir},%{_libdir}/qt/plugins-mt,%{_libdir}/qt/plugins-mt/qsa,%{_examplesdir}/%{name}}

##%if %{?_with_base:1}0
headers="qsa/qsaglobal.h qsa/qsobjectfactory.h qsa/qswrapperfactory.h qsa/qseditor.h qsa/qsproject.h qsa/qsinterpreter.h qsa/qsargument.h qsa/qsinputdialogfactory.h qsa/qsscript.h qsa/qsconfig.h ide/qsworkbench.h"

for i in $headers; do
	install src/$i     $RPM_BUILD_ROOT%{_includedir}
done

install 

install src/qsa/qsa.prf	$RPM_BUILD_ROOT%{_datadir}/qt/mkspecs/linux-g++/
install src/qsa/libqsa.so.1.0.0	$RPM_BUILD_ROOT%{_libdir}
cd $RPM_BUILD_ROOT%{_libdir}
ln -s libqsa.so.1.0.0 libqsa.so 
ln -s libqsa.so.1.0.0 libqsa.so.1 
ln -s libqsa.so.1.0.0 libqsa.so.1.0
install $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/designer/
cp -rf examples/ $RPM_BUILD_ROOT%{_examplesdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post 

%preun 

%files 
%defattr(644,root,root,755)
%doc doc/html/* 
%attr(755,root,root) %{_libdir}/lib*.so.*
%{_libdir}/qt/plugins-mt/designer/*

%files devel
%defattr(644,root,root,755)
%{_datadir}/qt/mkspecs/linux-g++/*
%{_includedir}/*
%{_libdir}/lib*.so

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}
