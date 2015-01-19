%define subver	fadf11e
%define rel		1
Summary:	Wiimote interface library
Name:		cwiid
Version:	0.6.00
Release:	0.%{rel}.%{subver}
License:	GPL v2+
Group:		Libraries
#Source0:	https://github.com/abstrakraft/cwiid/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/abstrakraft/cwiid/archive/%{subver}/%{name}-%{version}-%{subver}.tar.gz
# Source0-md5:	2d5430a465357242514942ae82139609
Source1:	wmgui.desktop
Patch0:		wmdemo-lib.patch
URL:		http://abstrakraft.org/cwiid/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	bluez-libs-devel
BuildRequires:	desktop-file-utils
BuildRequires:	flex
BuildRequires:	gawk
BuildRequires:	gtk+2-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 2.4
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CWiiD is a library that enables your application to communicate with a
wiimote using a bluetooth connection.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bluez-libs-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n python-%{name}
Summary:	Python binding for %{name}
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Obsoletes:	cwiid-python2

%description -n python-%{name}
Python2 binding for %{name}

%package utils
Summary:	Wiimote connection test application
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-wmgui = %{version}-%{release}
Obsoletes:	cwiid-wmgui < 0.6.00-7

%description utils
Applications to test the wiimote connection

%package wminput
Summary:	Enables using the wiimote as an input source
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

%prep
%setup -qc
mv %{name}-*/* .
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
CC="%{__cc} %{rpmcflags}"
%configure \
	--disable-ldconfig
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

rm -v $RPM_BUILD_ROOT%{_libdir}/libcwiid.a

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
%{_includedir}/cwiid.h
%{_libdir}/libcwiid.so
%{_pkgconfigdir}/cwiid.pc

%files -n python-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/cwiid.so
%{py_sitedir}/cwiid-%{version}-py*.egg-info

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

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lswm
%attr(755,root,root) %{_bindir}/wmgui
%{_mandir}/man1/wmgui.1*
%{_desktopdir}/wmgui.desktop
