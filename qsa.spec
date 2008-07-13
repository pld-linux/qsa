Summary:	Qt Script for Applications
Summary(pl.UTF-8):	Qt Script for Applications - język skryptowy dla aplikacji Qt
Name:		qsa
Version:	1.1.3
Release:	2
License:	GPL v2
Group:		X11/Libraries
Source0:	ftp://ftp.trolltech.com/qsa/source/%{name}-x11-free-%{version}.tar.gz
# Source0-md5:	3d05e0ab9b15ccdce7517d7c9653d623
Source1:	%{name}-doc
Patch0:		%{name}-buildsystem.patch
URL:		http://www.trolltech.com/products/qsa/index.html
BuildRequires:	qmake
BuildRequires:	qt-devel >= 6:3.1.1-4
BuildRequires:	sed >= 4.0
Requires:	qt >= 3.1.1-4
Obsoletes:	qsa-examples
Obsoletes:	qsa-lib-devel
Obsoletes:	qsa-libs
Obsoletes:	qt-plugin-qsa-quickcustom
Obsoletes:	qt-plugin-qsa-quickide
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautocompressdoc 	*.xml

%description
QSA is a Qt extension that allows developers to make their C++
applications scriptable using an interpreted scripting language, Qt
Script (based on ECMAScript/JavaScript).

%description -l pl.UTF-8
QSA jest rozszerzeniem Qt, które umożliwia programistom tworzenie
aplikacji C++, które mogą być kontrolowane za pomocą intepretowanego
języka Qt Script (opartego o ECMAScript/JavaScript).

%package doc
Summary:	Documentation for QSA
Summary(pl.UTF-8):	Dokumentacja dla QSA
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for Qt Script in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do Qt Script w formacie HTML.

%package devel
Summary:	QSA - header files
Summary(pl.UTF-8):	QSA - pliki nagłówkowe
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	qt-devel

%description devel
Header files for applications using Qt Script.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla aplikacji wykorzystujących Qt Script.

%package examples
Summary:	QSA - examples for developers
Summary(pl.UTF-8):	QSA - przykładowe programy dla programistów
Group:		X11/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	qt-devel

%description examples
Examples of Qt Script usage for developers.

%description examples -l pl.UTF-8
Przykładowe sposoby wykorzystania Qt Script dla programistów.

%package -n qt-plugin-designer-qsa
Summary:	Qt Script for Applications - Qt Designer plugin
Summary(pl.UTF-8):	System skryptowania Qt - wtyczka do Qt Designera
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	qt-designer-libs

%description -n qt-plugin-designer-qsa
A Qt Designer plugin allowing the use of Qt Script while developing
GUI.

%description -n qt-plugin-designer-qsa -l pl.UTF-8
Wtyczka do Qt Designer umożliwiająca wykorzystywanie Qt Script podczas
tworzenia interfejsu graficznego.

%prep
%setup -q -n %{name}-x11-free-%{version}
%patch0 -p1

%build
export QTDIR=%{_prefix}
export QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++
export LD_LIBRARY_PATH="`/bin/pwd`/src/qsa:$LD_LIBRARY_PATH"

find . -name Makefile -exec rm {} \;

export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcflags}"
CONF="CONFIG+=xml table sql network thread"

cd src/qsa

rm -rf qsconfig.h
cat >> qsconfig.h << EOF
#ifndef QS_CONFIG_H
#define QS_CONFIG_H
/* Trolltech sucks */
#endif
EOF

$QTDIR/bin/qmake "$CONF"
%{__make}

cd ../plugin

$QTDIR/bin/qmake "$CONF"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/qt/mkspecs/linux-g++
install -d $RPM_BUILD_ROOT{%{_includedir}/qsa,%{_libdir}/qt/plugins-mt/designer}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}
install -d $RPM_BUILD_ROOT%{_docdir}/qsa/html
install -d $RPM_BUILD_ROOT%{_bindir}

cp -df lib/* $RPM_BUILD_ROOT%{_libdir}

install plugins/designer/libqseditorplugin.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/designer

headers="qsa/qsaglobal.h qsa/qsobjectfactory.h qsa/qswrapperfactory.h \
	qsa/qseditor.h qsa/qsproject.h qsa/qsinterpreter.h qsa/qsargument.h \
	qsa/qsinputdialogfactory.h qsa/qsutilfactory.h qsa/qsscript.h \
	qsa/qsconfig.h ide/qsworkbench.h"

for i in $headers; do
	install src/$i $RPM_BUILD_ROOT%{_includedir}/qsa
done

install src/qsa/qsa.prf	$RPM_BUILD_ROOT%{_datadir}/qt/mkspecs/linux-g++
cp -rf examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}

Z=$PWD

cd $RPM_BUILD_ROOT%{_examplesdir}/%{name}
rm -rf qsa.prf
export QTDIR=%{_usr}
export QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++
$QTDIR/bin/qmake

for i in console filter game scribblescripter scriptbutton spreadsheet textedit wrappers;
do
	sed -i -e "s,\.\./qsa,qsa," $i/$i.pro;
#	cd $i
#	$QTDIR/bin/qmake
#	cd ..
done

cd $Z

cp -rf doc/html/* $RPM_BUILD_ROOT%{_docdir}/qsa/html
install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post doc
echo "######################################################"
echo "# Please run the 'qsa-doc -add' command for every    #"
echo "# user who wants to have access to QSA documentation #"
echo "#         from the Qt Assistant.                     #"
echo "######################################################"

%postun doc
if [ "$1" = "0" ]; then
echo "###########################################################"
echo "# Please run the 'qsa-doc -remove' command for every user #"
echo "# for whom you ran 'qsa-doc -add' earlier in order to     #"
echo "#    remove qsa documentation from the Qt Assistant.      #"
echo "###########################################################"
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files doc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qsa-doc
%dir %{_docdir}/qsa
%dir %{_docdir}/qsa/html
%{_docdir}/qsa/html/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_datadir}/qt/mkspecs/linux-g++/*
%{_includedir}/qsa

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}

%files -n qt-plugin-designer-qsa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt/plugins-mt/designer/*
