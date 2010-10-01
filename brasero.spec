#
# Conditinal build:
%bcond_without	beagle		# disable beagle search
#
Summary:	Disc burning application for GNOME
Summary(pl.UTF-8):	Program do wypalania płyt dla GNOME
Name:		brasero
Version:	2.32.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/brasero/2.32/%{name}-%{version}.tar.bz2
# Source0-md5:	09aaa188f33caa0bcc71a7dfc4a3f9ad
URL:		http://www.gnome.org/projects/brasero/
BuildRequires:	GConf2-devel >= 2.32.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	glibc-misc
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-doc-utils
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	gstreamer-devel >= 0.10.15
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:	gtk+2-devel >= 2:2.22.0
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	intltool >= 0.40.0
%{?with_beagle:BuildRequires:	libbeagle-devel >= 0.3.0}
BuildRequires:	libburn-devel >= 0.4.0
BuildRequires:	libcanberra-devel
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	libisofs-devel >= 0.6.4
BuildRequires:	libtool
BuildRequires:	libunique-devel >= 1.0.0
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	nautilus-devel >= 2.26.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	totem-pl-parser-devel >= 2.30.0
BuildRequires:	tracker-devel >= 0.8.0
BuildRequires:	xorg-lib-libSM-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires:	%{name}-libs = %{version}-%{release}
Suggests:	dvd+rw-tools
Suggests:	gstreamer-audio-effects-base
Suggests:	gstreamer-audio-effects-good
Obsoletes:	bonfire
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Brasero is a CD/DVD mastering tool for the GNOME desktop. It is
designed to be simple and easy to use.

%description -l pl.UTF-8
Brasero jest narzędziem do masteringu płyt CD/DVD dla biurka GNOME.
Jest zaprojektowany by być prostym i łatwym w obsłudze.

%package libs
Summary:	Brasero library
Summary(pl.UTF-8):	Biblioteka Brasero
Group:		X11/Libraries

%description libs
Brasero library.

%description libs -l pl.UTF-8
Biblioteka Brasero.

%package devel
Summary:	Header files for Brasero library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Brasero
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.26.0
Requires:	gtk+2-devel >= 2:2.22.0

%description devel
Header files for Brasero library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Brasero.

%package apidocs
Summary:	Brasero library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Brasero
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Brasero library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Brasero.

%package -n nautilus-extension-brasero
Summary:	Brasero extension for Nautilus
Summary(pl.UTF-8):	Rozszerzenie Brasero dla Nautilusa
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus >= 2.26.0

%description -n nautilus-extension-brasero
Adds Brasero integration to Nautilus.

%description -n nautilus-extension-brasero -l pl.UTF-8
Dodaje integrację Brasero z Nautilusem.

%prep
%setup -q
sed -i s#^en@shaw## po/LINGUAS
rm po/en@shaw.po

%build
%{__gtkdocize}
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_beagle:--disable-search} \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--disable-caches \
	--disable-schemas-install \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/brasero/plugins/lib*.{la,a}
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/*.{la,a}

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor
glib-compile-schemas %{_datadir}/glib-2.0/schemas

%postun
%update_desktop_database_postun
%update_mime_database
%update_icon_cache hicolor
glib-compile-schemas %{_datadir}/glib-2.0/schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post -n nautilus-extension-brasero
%update_desktop_database_post

%postun -n nautilus-extension-brasero
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/brasero
%{_datadir}/%{name}
%{_datadir}/mime/packages/%{name}.xml
%dir %{_libdir}/brasero
%dir %{_libdir}/brasero/plugins
%attr(755,root,root) %{_libdir}/brasero/plugins/lib*.so
%{_datadir}/GConf/gsettings/brasero.convert
%{_datadir}/glib-2.0/schemas/org.gnome.brasero.gschema.xml
%{_desktopdir}/brasero.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_mandir}/man1/brasero.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbrasero-burn.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbrasero-burn.so.1
%attr(755,root,root) %{_libdir}/libbrasero-media.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbrasero-media.so.1
%attr(755,root,root) %{_libdir}/libbrasero-utils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbrasero-utils.so.1
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbrasero-burn.so
%attr(755,root,root) %{_libdir}/libbrasero-media.so
%attr(755,root,root) %{_libdir}/libbrasero-utils.so
%{_includedir}/brasero
%{_pkgconfigdir}/libbrasero-burn.pc
%{_pkgconfigdir}/libbrasero-media.pc
%{_datadir}/gir-1.0/*.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libbrasero-burn
%{_gtkdocdir}/libbrasero-media

%files -n nautilus-extension-brasero
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-2.0/libnautilus-brasero-extension.so
%{_desktopdir}/brasero-nautilus.desktop
