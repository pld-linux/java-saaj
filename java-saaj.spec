%bcond_without  javadoc         # don't build javadoc

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif

%define 	srcname	saaj
%include	/usr/lib/rpm/macros.java
Summary:	SAAJ Standard Implementation
Name:		java-%{srcname}
Version:	1.3.2
Release:	1
License:	CDDL v1.0 and GPL v2
Group:		Libraries/Java
Source0:	https://saaj.dev.java.net/files/documents/52/125659/saaj%{version}.src.zip
# Source0-md5:	11eb6e620f65bced00471dc5388c4dad
URL:		https://saaj.dev.java.net/
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SAAJ supports both SOAP 1.1 and SOAP 1.2.

%package javadoc
Summary:	Online manual for saaj
Summary(pl.UTF-8):	Dokumentacja online do saaj
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for saaj.

%description javadoc -l pl.UTF-8
Dokumentacja do saaj.

%description javadoc -l fr.UTF-8
Javadoc pour saaj.

%prep
%setup -qc

%build

install -d build
%javac -d build $(find -name '*.java')

%if %{with javadoc}
%javadoc -d apidocs \
	%{?with_java_sun:com.sun.xml.messaging.saaj} \
	$(find com/sun/xml/messaging/saaj/ -name '*.java')
%endif

%jar -cf %{srcname}-%{version}.jar -C build .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
