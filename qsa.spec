#
# DONT BUILD THIS AS ROOT! JUST DONT! IF YOU DO, DONT BLAME ME.
#
# _with_base		trolltech is magic (this generates qsa only
#			after this you can rebuild it)
#
# Trolltech sucks
%define 	_noautocompressdoc 	*.xml
%define 	_status		beta3
Summary:	Qt Script for Applications
Summary(pl):	System skryptowania Qt
Name:		qsa
Version:	1.0
Release:	0.%{_status}.1
License:	GPL
Group:		X11/Libraries
Source0:	ftp://ftp.trolltech.com/qsa/%{name}-x11-free-%{_status}.tar.gz
# Source0-md5:	2264ccc24deff8333f553895138b227b
Patch0:		%{name}-buildsystem.patch
URL:		http://www.trolltech.com/products/qsa/index.html
%{!?_with_base:BuildRequires:	qsa-lib-devel = %{version}}
BuildRequires:	qt-devel >= 3.1.1-4
BuildRequires:	sed >= 4.0
%{!?_with_base:Requires:	qsa-lib = %{version}}
Requires:	qt >= 3.1.1-4
# to obtain this use _with_base
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
Requires:	qt >= 3.2-0.030405.4

%description libs
Qt Script for Applications - libraries.

%description libs -l pl
System skryptowania Qt - biblioteki.

%package devel
Summary:	QSA - headers for libraries
Summary(pl):	QSA - pliki nag³ówkowe dla bibliotek
Group:		X11/Libraries
Requires:	qsa-libs = %{version}
Requires:	qt-devel >= 3.2-0.030405.4

%description devel
Qt Script for Applications - headers for libraries.

%description devel -l pl
System skryptowania Qt - pliki nag³ówkowe dla bibliotek.

%package examples
Summary:	QSA - examples for developers
Summary(pl):	QSA - przyk³adowe programy dla programistów
Group:		X11/Libraries

%description examples
Qt Script for Applications - examples for developers.

%description examples -l pl
System skryptowania Qt - przyk³adowe programy dla programistów.

%package -n qt-plugin-qsa-quickide
Summary:	QSA - no idea what this is.
Group:		X11/Libraries
Requires:	qsa-libs = %{version}

%description -n qt-plugin-qsa-quickide
Qt Script for Applications - ?.

%package -n qt-plugin-qsa-quickcustom
Summary:	QSA - no idea what this is.
Group:		X11/Libraries
Requires:	qsa-libs = %{version}

%description -n qt-plugin-qsa-quickcustom
Qt Script for Applications - ?.

%prep
%setup -q -n %{name}-x11-free-%{_status}
%patch0 -p1

%build
# Fuck trolltechs build system ideas
export QTDIR=%{_usr}
export QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++/
find . -name Makefile -exec rm {} \;

%if %{?_with_base:1}0
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcflags}"
CONF="CONFIG+=thread"
cd src/qsa
qmake "${CONF}" qsa.pro
%{__make}
%endif

%if %{?!_with_base:1}%{?_with_base:0}
CONF="CONFIG+=thread"
cd src/ide; qmake "${CONF}"
%{__make}

cd ../custom
qmake "${CONF}"
%{__make}

cd ../../examples
qmake "${CONF}"
%endif

%install
rm -rf  $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_datadir}/qt/mkspecs/linux-g++,%{_includedir},%{_libdir}/qt/plugins-mt,%{_libdir}/qt/plugins-mt/qsa,%{_examplesdir}/%{name}}

%if %{?_with_base:1}0
install src/qsa/*.h 	$RPM_BUILD_ROOT%{_includedir}
install src/qsa/qsa.prf	$RPM_BUILD_ROOT%{_datadir}/qt/mkspecs/linux-g++/
install src/qsa/libqsa.so.1.0.0	$RPM_BUILD_ROOT%{_libdir}
cd $RPM_BUILD_ROOT%{_libdir}
ln -s libqsa.so.1.0.0 libqsa.so
ln -s libqsa.so.1.0.0 libqsa.so.1
ln -s libqsa.so.1.0.0 libqsa.so.1.0
%endif

%if 0%{!?_with_base:1}
install src/ide/libquickide.so	$RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/qsa/
install src/custom/libquickcustom.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/qsa/
cp -rf examples/ $RPM_BUILD_ROOT%{_examplesdir}/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post libs
assistant -addContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qsa.xml
assistant -addContentFile %{_defaultdocdir}/%{name}-lib-%{version}/language.xml
assistant -addContentFile %{_defaultdocdir}/%{name}-lib-%{version}/language.xml
assistant -addContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qt-script-for-applications.xml
assistant -addContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qsa-designer.xml

%preun libs
assistant -removeContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qsa.xml
assistant -removeContentFile %{_defaultdocdir}/%{name}-lib-%{version}/language.xml
assistant -removeContentFile %{_defaultdocdir}/%{name}-lib-%{version}/language.xml
assistant -removeContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qt-script-for-applications.xml
assistant -removeContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qsa-designer.xml

%if 0%{?_with_base:1}
%files libs
%defattr(644,root,root,755)
%doc doc/html/qsa.xml doc/html/language.xml doc/html/language.xml doc/html/qsa-designer.xml doc/html/qt-script-for-applications.xml
%attr(755,root,root) %{_libdir}/lib*.so.*
%endif

%if 0%{?_with_base:1}
%files devel
%defattr(644,root,root,755)
%{_datadir}/qt/mkspecs/linux-g++/*
%{_includedir}/*
%{_libdir}/lib*.so
%endif

%if 0%{!?_with_base:1}
%files -n qt-plugin-qsa-quickide
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt/plugins-mt/qsa/libquickide.so

%files -n qt-plugin-qsa-quickcustom
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt/plugins-mt/qsa/libquickcustom.so

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}
%endif
