%{?scl:%scl_package junit-addons}
%{!?scl:%global pkg_name %{name}}

Name:          %{?scl_prefix}junit-addons
Version:       1.4
Release:       14.1%{?dist}
Summary:       JUnitX helper classes for JUnit
License:       ASL 1.1
Url:           http://sourceforge.net/projects/junit-addons/
Source0:       http://sourceforge.net/projects/%{pkg_name}/files/JUnit-addons/JUnit-addons%20%{version}/%{pkg_name}-%{version}.zip
# from http://junit-addons.cvs.sourceforge.net/viewvc/junit-addons/junit-addons/build.xml?view=markup&pathrev=release_1_4
Source1:       %{pkg_name}-build.xml
Source2:       http://mirrors.ibiblio.org/pub/mirrors/maven2/%{pkg_name}/%{pkg_name}/%{version}/%{pkg_name}-%{version}.pom
Patch0:        junit-addons-1.4-enum.patch

BuildRequires: %{?scl_prefix}javapackages-local
BuildRequires: %{?scl_prefix}ant
BuildRequires: %{?scl_prefix}apache-commons-logging
BuildRequires: %{?scl_prefix}jaxen
BuildRequires: %{?scl_prefix}jdom
BuildRequires: %{?scl_prefix}junit
BuildRequires: %{?scl_prefix}xerces-j2
BuildRequires: %{?scl_prefix}xml-commons-apis

Requires:      %{?scl_prefix}ant
Requires:      %{?scl_prefix}jaxen
Requires:      %{?scl_prefix}jdom
Requires:      %{?scl_prefix}junit
Requires:      %{?scl_prefix}xerces-j2

BuildArch:     noarch

%description
JUnit-addons is a collection of helper classes for JUnit. 

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%setup -n %{pkg_name}-%{version} -q

%jar xf src.jar
find . -name "*.class" -delete
find . -type f -name "*.jar" -delete
find . -type f -name "*.zip" -delete

%patch0 -p0

rm -r api
cp -p %{SOURCE1} build.xml

# fix non ASCII chars
for s in src/main/junitx/framework/TestSuite.java;do
  native2ascii -encoding UTF8 ${s} ${s}
done

# disable test
# some tests fails with the regenerate test resource
# tests.jar
# tests.zip
sed -i "s| test, ||" build.xml

%build
# regenerate test resource
#(
#  cd src/example
#  mkdir test
#  javac -d test -source 1.4 -target 1.4 $(find . -name "*.java") -cp $(build-classpath junit4)
#  rm test/junitx/example/*.class
#  cp -p junitx/example/packageA/SampleA.txt test/junitx/example/packageA/
#  cp -p junitx/example/packageA/packageB/SampleB.txt test/junitx/example/packageA/packageB/
#  (
#    cd test
#    jar -cf ../tests.jar *
##    zip -r ../tests.zip *
#  )
#  cp -p tests.jar tests.zip
#  rm -r test
#)

export CLASSPATH=
export OPT_JAR_LIST=:
%ant \
  -Dant.build.javac.source=1.6 \
  -Djdom.jar=$(build-classpath jdom) \
  -Djaxen.jar=$(build-classpath jaxen) \
  -Dsaxpath.jar=$(build-classpath jaxen) \
  -Dant.jar=$(build-classpath ant.jar) \
  -Djunit.jar=$(build-classpath junit) \
  -Dxerces.jar=$(build-classpath xerces-j2) \
  -Dxml-apis.jar=$(build-classpath xml-commons-apis) \
  -Dcommons-logging.jar=$(build-classpath commons-logging) \
  -Dproject.name=%{pkg_name} \
  -Dproject.version=%{version} \
  release

%install
%mvn_file : %{pkg_name}
%mvn_artifact %{SOURCE2} dist/%{pkg_name}-%{version}.jar

%mvn_install -J build/api

%files -f .mfiles
%doc README WHATSNEW
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 1.4-14.1
- Automated package import and SCL-ization

* Wed Mar 22 2017 Michael Simacek <msimacek@redhat.com> - 1.4-14
- Install with XMvn

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 09 2015 gil cattaneo <puntogil@libero.it> 1.4-10
- use javac source/target 1.6

* Mon Feb 09 2015 gil cattaneo <puntogil@libero.it> 1.4-9
- introduce license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 gil cattaneo <puntogil@libero.it> 1.4-7
- Use .mfiles generated during build
- Fix junit dep

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.4-6
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 gil cattaneo <puntogil@libero.it> 1.4-2
- remove pre-compiled artefacts
- add requires ant, jaxen, jdom

* Sat May 05 2012 gil cattaneo <puntogil@libero.it> 1.4-1
- initial rpm
