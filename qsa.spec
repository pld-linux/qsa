#
# _with_base		trolltech is magic (this generates qsa only
#			after this you can rebuild it)
#
# Trolltech sucks
%define 	_noautocompressdoc 	*.xml
%define 	_status		beta2
Summary:	Qt Script for Applications
Summary(pl): 	System skryptowania Qt
Name:		qsa
Version:	1.0
Release:	0.%{_status}.2
License:	GPL
Group:		X11/Libraries
Source0:	ftp://ftp.trolltech.com/qsa/%{name}-x11-free-%{_status}.tar.gz

URL:		http://www.trolltech.com/products/qsa/index.html
BuildRequires:	qt-devel >= 3.1.1-4
%{!?_with_base:BuildRequires: qsa-lib-devel = %{version}}
%{!?_with_base:Requires:	qsa-lib = %{version}}
Requires:	qt >= 3.1.1-4
# to obtain this use _with_base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt Script for Applications

%description -l pl
System skryptowania Qt


%package lib
Summary:	QSA - libraries
Summary(pl):	QSA - biblioteki
Group:		X11/Libraries
Requires(post,preun): qt-utils

%description lib
Qt Script for Applications - libraries

%description lib -l pl
System skryptowania Qt - biblioteki

%package lib-devel
Summary:        QSA - headers for libraries
Summary(pl):    QSA - nag³ówki dla bibliotek
Group:          X11/Libraries
Requires: 	qsa-lib = %{version}

%description lib-devel
Qt Script for Applications - headers for libraries

%description lib-devel -l pl
System skryptowania Qt - nag³ówki dla bibliotek

%prep
%setup -q -n %{name}-x11-free-%{_status}

%build
# Fuck trolltechs build system ideas
export QTDIR=%{_usr}
export QMAKESPEC=%{_datadir}/qt/mkspecs/linux-g++/
find . -name Makefile -exec rm {} \;
# do only a threaded build (making an st version 
# would make compiling qsa apps much more complicated

#cd examples; qmake "${CONF}")
#cd src/custom; qmake "${CONF}"
#cd src/ide; qmake "${CONF}")

%if %{?_with_base:1}0
CONF="CONFIG+=thread"
cd src/qsa
qmake "${CONF}" qsa.pro
sed -i -e "s,all: Makefile,all:,g" Makefile
grep -v MOVE Makefile >> Makefile.1
grep -v DEL_FILE Makefile.1 >> Makefile
%{__make}
mv -f libqsa.so.1.0.0 libqsa-mt.so.1.0.0
rm -rf libqsa.so*

CONF=""
qmake "${CONF}" qsa.pro
%{__make} clean
sed -i -e "s,all: Makefile,all:,g" Makefile
grep -v MOVE Makefile >> Makefile.1
grep -v DEL_FILE Makefile.1 >> Makefile
%{__make}
%endif

%if %{?!_with_base:1}%{?_with_base:0}
cd examples; qmake "${CONF}"
cd src/custom; qmake "${CONF}"
cd src/ide; qmake "${CONF}"
sed -i -e "s,all: Makefile,all:,g" Makefile
grep -v MOVE Makefile >> Makefile.1
cat Makefile.1|grep -v "`cat Makefile.1|grep test|grep QTD`" >> Makefile.2
grep -v DEL_FILE Makefile.2 >> Makefile
%{__make}

cd ../custom
sed -i -e "s,all: Makefile,all:,g" Makefile
grep -v MOVE Makefile >> Makefile.1
cat Makefile.1|grep -v "`cat Makefile.1|grep test|grep QTD`" >> Makefile.2
grep -v DEL_FILE Makefile.2 >> Makefile
%{__make}
%endif 

%install
rm -rf  $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_usr},%{_bindir},%{_libdir},%{_datadir},%{_datadir}/qt,%{_datadir}/qt/mkspecs,%{_datadir}/qt/mkspecs/linux-g++,%{_includedir},%{_libdir}/qt/plugins-mt,%{_examplesdir},%{_examplesdir}/%{name}}

%if %{?_with_base:1}0
install src/qsa/*.h 	$RPM_BUILD_ROOT%{_includedir}
install src/qsa/qsa.prf	$RPM_BUILD_ROOT%{_datadir}/qt/mkspecs/linux-g++/
install src/qsa/libqsa.so.1.0.0	$RPM_BUILD_ROOT%{_libdir}
install src/qsa/libqsa-mt.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}
cd $RPM_BUILD_ROOT%{_libdir}
ln -s libqsa.so.1.0.0 libqsa.so 
ln -s libqsa.so.1.0.0 libqsa.so.1 
ln -s libqsa.so.1.0.0 libqsa.so.1.0
ln -s libqsa-mt.so.1.0.0 libqsa-mt.so
ln -s libqsa-mt.so.1.0.0 libqsa-mt.so.1
ln -s libqsa-mt.so.1.0.0 libqsa-mt.so.1.0
%endif

%if %{?!_with_base:1}%{?_with_base:0}
install src/ide/libquickide.so	$RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/
install src/ide/libquickcustom.so $RPM_BUILD_ROOT%{_libdir}/qt/plugins-mt/
install examples/ %{_examplesdir}/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post lib
assistant -addContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qsa.xml
assistant -addContentFile %{_defaultdocdir}/%{name}-lib-%{version}/language.xml
assistant -addContentFile %{_defaultdocdir}/%{name}-lib-%{version}/language.xml
assistant -addContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qt-script-for-applications.xml
assistant -addContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qsa-designer.xml

%preun lib
assistant -removeContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qsa.xml
assistant -removeContentFile %{_defaultdocdir}/%{name}-lib-%{version}/language.xml
assistant -removeContentFile %{_defaultdocdir}/%{name}-lib-%{version}/language.xml
assistant -removeContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qt-script-for-applications.xml
assistant -removeContentFile %{_defaultdocdir}/%{name}-lib-%{version}/qsa-designer.xml

%files lib
%if %{?_with_base:1}0
%defattr(644,root,root,755)
%doc doc/html/qsa.xml doc/html/language.xml doc/html/language.xml doc/html/qsa-designer.xml doc/html/qt-script-for-applications.xml
%attr(755,root,root) %{_libdir}/lib*.so.*
%endif

%files lib-devel
%if %{?_with_base:1}0
%{_datadir}/qt/mkspecs/linux-g++/*
%{_includedir}/*
%{_libdir}/lib*.so
%endif

##%files subpackage
##%defattr(644,root,root,755)
##%doc extras/*.gz
##%{_datadir}/%{name}-ext
