#
# Conditional build:
%bcond_without	python2		# python (2.x) binding
%bcond_without	static_libs	# static library

%define gitref	fadf11e
%define	snap	20100222
%define rel	1
Summary:	Wiimote interface library
Summary(pl.UTF-8):	Biblioteka interfejsu Wiimote
Name:		cwiid
Version:	0.6.00
Release:	1.%{snap}.%{rel}
License:	GPL v2+
Group:		Libraries
#Source0:	https://github.com/abstrakraft/cwiid/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/abstrakraft/cwiid/archive/%{gitref}/%{name}-%{version}-%{gitref}.tar.gz
# Source0-md5:	2d5430a465357242514942ae82139609
Source1:	wmgui.desktop
Patch0:		wmdemo-lib.patch
Patch1:		%{name}-format.patch
URL:		https://github.com/abstrakraft/cwiid
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	bluez-libs-devel
BuildRequires:	desktop-file-utils
BuildRequires:	flex
BuildRequires:	gawk
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-devel >= 2.4}
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CWiiD is a library that enables your application to communicate with a
wiimote using a Bluetooth connection.

%description -l pl.UTF-8
CWiiD to bibliotka umożliwiająca aplikacjom komunikację z wiimote przy
użyciu połączenia Bluetooth.

%package devel
Summary:	Development files for CWiiD
Summary(pl.UTF-8):	Pliki programistyczne CWiiD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bluez-libs-devel

%description devel
This package contains header files for developing applications that
use CWiiD.

%description devel -l pl.UTF-8
Ten pakiet zaweira pliki nagłówkowe do tworzenia aplikacji
wykorzystujących CWiiD.

%package static
Summary:	Static CWiiD library
Summary(pl.UTF-8):	Statyczna biblioteka CWiiD
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CWiiD library.

%description static -l pl.UTF-8
Statyczna biblioteka CWiiD.

%package -n python-%{name}
Summary:	Python binding for CWiiD library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki CWiiD
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Obsoletes:	cwiid-python2 < 0.6.00-1

%description -n python-%{name}
Python2 binding for CWiiD library.

%description -n python-%{name} -l pl.UTF-8
Wiązania Pythona do biblioteki CWiiD.

%package utils
Summary:	Wiimote connection test applications
Summary(pl.UTF-8):	Aplikacje testujące połączenie Wiimote
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-wmgui = %{version}-%{release}
Obsoletes:	cwiid-wmgui < 0.6.00-7

%description utils
Applications to test the wiimote connection.

%description utils -l pl.UTF-8
Aplikacje do testowania połączenia wiimote.

%package wminput
Summary:	Enables using the wiimote as an input source
Summary(pl.UTF-8):	Użycie wiimote jako źródła wejścia
# The licence must be GPLv2 instead of GPLv2+ for this package
# since the file wminput/action_enum.txt is GPLv2 as stated
# in the file.
License:	GPL v2
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	python-%{name} = %{version}-%{release}

%description wminput
This program allows the user to use the wiimote to emulate normal
system input sources like the mouse and keyboard.

%description wminput -l pl.UTF-8
Ten program pozwala użytkownikowi używać wiimote do emulacji zwykłych
źródeł wejściowych, takich jak mysz i klawiatura.

%prep
%setup -qc
%{__mv} %{name}-*/* .
%patch -P0 -p1
%patch -P1 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	PYTHON=%{__python} \
	--disable-ldconfig \
	%{!?with_python:--without-python}

LDFLAGS="%{rpmldflags}" \
%{__make} \
	WARNFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -W"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%if %{without static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcwiid.a
%endif

desktop-file-install --dir=$RPM_BUILD_ROOT%{_desktopdir} %{SOURCE1}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README COPYING ChangeLog
%attr(755,root,root) %{_libdir}/libcwiid.so.1.0
%ghost %{_libdir}/libcwiid.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcwiid.so
%{_includedir}/cwiid.h
%{_pkgconfigdir}/cwiid.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcwiid.a
%endif

%if %{with python2}
%files -n python-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/cwiid.so
%{py_sitedir}/cwiid-%{version}-py*.egg-info
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lswm
%attr(755,root,root) %{_bindir}/wmgui
%{_mandir}/man1/wmgui.1*
%{_desktopdir}/wmgui.desktop

%files wminput
%defattr(644,root,root,755)
%doc doc/Xmodmap doc/wminput.list
%dir %{_sysconfdir}/cwiid
%dir %{_sysconfdir}/cwiid/wminput
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cwiid/wminput/acc_led
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cwiid/wminput/acc_ptr
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cwiid/wminput/buttons
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cwiid/wminput/default
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cwiid/wminput/gamepad
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cwiid/wminput/ir_ptr
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cwiid/wminput/neverball
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cwiid/wminput/nunchuk_acc_ptr
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cwiid/wminput/nunchuk_stick2btn
%attr(755,root,root) %{_bindir}/wminput
%{_mandir}/man1/wminput.1*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/acc.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/ir_ptr.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/led.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/nunchuk_acc.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/nunchuk_stick2btn.so
