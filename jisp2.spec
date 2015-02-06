# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section free
%define jisp_version 2.5.1
%define gcj_support 1

Name:           jisp2
Version:        2.5.1
Release:        4.0.8
Epoch:          0
Summary:        Java Indexed Serialization Package
License:        GPL-like
URL:            http://www.coyotegulch.com/products/jisp/
Group:          Development/Java
Source0:        jisp-%{version}-source.tar.gz
Patch0:         jisp2-2.5.1-makefile.patch
# jisp-3.0.0 won't work with jakarta-turbine-jcs
BuildRequires:  java-rpmbuild >= 0:1.7
Requires:  jpackage-utils >= 0:1.7
Provides:  hibernate_in_process_cache = %{epoch}:%{version}-%{release}
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Jisp uses B-Tree and hash indexes for keyed access to variable-length 
serialized objects stored in files. 

%package demo
Summary:        Demo for %{name}
Group:          Development/Java

%description demo
Demo for %{name}

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n jisp-%{version}
%{__perl} -pi -e 's/\r$//g' svfl.txt
%patch0 -p1

%build
export CLASSPATH=
%{__make} JAVA=%{java} JAVAC=%{javac} JCFLAGS="-classpath . -nowarn" JAR=%{jar} JAVADOC=%{javadoc} JispDemo jars docs

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p jisp.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/lib
cp -a jisp-demo.jar $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/lib
# XXX: could thie be right?
cp -a *.java $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -a *.txt $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

# hibernate_in_process_cache ghost symlink
ln -s %{_sysconfdir}/alternatives \
  $RPM_BUILD_ROOT%{_javadir}/hibernate_in_process_cache.jar

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-alternatives --install %{_javadir}/hibernate_in_process_cache.jar \
  hibernate_in_process_cache %{_javadir}/%{name}.jar 30
%if %{gcj_support}
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif
  
%preun
{
  [ $1 -eq 0 ] || exit 0
  update-alternatives --remove hibernate_in_process_cache %{_javadir}/%{name}.jar
} >/dev/null 2>&1 || :

%files
%defattr(0644,root,root,0755)
%doc svfl.txt
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%ghost %{_javadir}/hibernate_in_process_cache.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.5.1-4.0.7mdv2011.0
+ Revision: 619829
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0:2.5.1-4.0.6mdv2010.0
+ Revision: 429626
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0:2.5.1-4.0.5mdv2009.0
+ Revision: 140829
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:2.5.1-4.0.4mdv2008.0
+ Revision: 87436
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Aug 18 2007 David Walluck <walluck@mandriva.org> 0:2.5.1-4.0.3mdv2008.0
+ Revision: 66453
- fix build
- do not use parallel make
- Import jisp2




* Thu Jul 26 2007 Alexander Kurtakov <akurtakov@active-lynx.com> - 0:2.5.1-4.0.1mdv2008.0
- Adapt for Mandriva

* Thu Jan 05 2006 Fernando Nasser <fnasser@redhat.com> - 0:2.5.1-4jpp
- First JPP 1.7 build

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:2.5.1-3jpp
- Rebuild with ant-1.6.2

* Fri Jul 02 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.5.1-2jpp
- Relax jpackage-utils versioned dependency
- Provide hibernate_in_process_cache and do update-alternatives, prio 30

* Tue Jan 27 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.5.1-1jpp
- First JPackage release
