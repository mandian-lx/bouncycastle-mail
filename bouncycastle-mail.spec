%{?_javapackages_macros:%_javapackages_macros}

%global ver  1.54
%global archivever  jdk15on-%(echo %{ver}|sed 's|\\\.||')

Summary:          S/MIME and CMS libraries for Bouncy Castle
Name:             bouncycastle-mail
Version:          %{ver}
Release:          1
License:          MIT
URL:              http://www.bouncycastle.org/

# Source tarball contains everything except test suite rousources
Source0:          http://www.bouncycastle.org/download/bcmail-%{archivever}.tar.gz
# Test suite resources are found in this jar
Source1:          http://www.bouncycastle.org/download/bctest-%{archivever}.jar

Source2:          http://repo2.maven.org/maven2/org/bouncycastle/bcmail-jdk15on/%{version}/bcmail-jdk15on-%{version}.pom
Source3:          bouncycastle-mail-OSGi.bnd

BuildArch:        noarch
BuildRequires:    aqute-bnd
BuildRequires:    java-devel
BuildRequires:    jpackage-utils
BuildRequires:    junit
BuildRequires:    mvn(org.bouncycastle:bcpkix-jdk15on) = %{version}
BuildRequires:    mvn(org.bouncycastle:bcprov-jdk15on) = %{version}
BuildRequires:    javamail
Requires:         mvn(org.bouncycastle:bcpkix-jdk15on) = %{version}
Requires:         mvn(org.bouncycastle:bcprov-jdk15on) = %{version}
Requires:         javamail

%description
Bouncy Castle consists of a lightweight cryptography API and is a provider 
for the Java Cryptography Extension and the Java Cryptography Architecture.
This library package offers additional classes, in particuar 
generators/processors for S/MIME and CMS, for Bouncy Castle.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for the %{name} package.

%prep
%setup -q -n bcmail-%{archivever}

# Unzip source and test suite resources
mkdir src
unzip -qq src.zip -d src/
unzip -qq %{SOURCE1} 'org/bouncycastle/mail/**' -x '**.class' '**.properties' -d src

cp -p %{SOURCE2} pom.xml

# Remove provided binaries
find . -type f -name "*.class" -delete
find . -type f -name "*.jar" -delete

cp -p %{SOURCE3} bcm.bnd
sed -i "s|@VERSION@|%{version}|" bcm.bnd

%mvn_file :bcmail-jdk15on bcmail
%mvn_alias :bcmail-jdk15on "org.bouncycastle:bcmail-jdk16"

%build
pushd src
  export CLASSPATH=$(build-classpath junit bcprov bcpkix javamail)
  javac -g -source 1.6 -target 1.6 -encoding UTF-8 $(find . -type f -name "*.java")
  jarfile="../bcmail.jar"
  # Exclude all */test/* , cf. upstream
  files="$(find . -type f \( -name '*.class' -o -name '*.properties' \) -not -path '*/test/*')"
  test ! -d classes && mf="" \
    || mf="`find classes/ -type f -name "*.mf" 2>/dev/null`"
  test -n "$mf" && jar cfm $jarfile $mf $files \
    || jar cf $jarfile $files
popd
java -jar $(build-classpath aqute-bnd) wrap -properties bcm.bnd bcmail.jar
mv bcmail.bar bcmail.jar
%mvn_artifact pom.xml bcmail.jar

%install
%mvn_install -J javadoc

%check
pushd src
  export CLASSPATH=$PWD:$(build-classpath junit hamcrest/core javamail bcprov bcpkix)
  for test in $(find . -name AllTests.class) ; do
    test=${test#./} ; test=${test%.class} ; test=${test//\//.}
    java org.junit.runner.JUnitCore $test
  done
popd

%files -f .mfiles
%doc CONTRIBUTORS.html index.html
%doc LICENSE.html

%files javadoc -f .mfiles-javadoc
%doc LICENSE.html

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 07 2016 Mat Booth <mat.booth@redhat.com> - 1.54-1
- Update to 1.54, fixes rhbz#1275175
- Install with mvn_install
- Allow tests to run

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 17 2015 gil cattaneo <puntogil@libero.it> 1.52-6
- remove the OSGi deprecated entry in bnd properties file

* Thu Jul 16 2015 Michael Simacek <msimacek@redhat.com> - 1.52-5
- Use aqute-bnd-2.4.1

* Tue Jun 23 2015 gil cattaneo <puntogil@libero.it> 1.52-4
- dropped the Export/Import-Package lists in the bnd properties file

* Thu Jun 18 2015 gil cattaneo <puntogil@libero.it> 1.52-3
- add OSGi metadata
- remove duplicate files

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 22 2015 Alexander Kurtakov <akurtako@redhat.com> 1.52-1
- Update to 1.52.
- Bump source/target to 1.6 as 1.5 is to be removed in Java 9.

* Fri Feb 13 2015 gil cattaneo <puntogil@libero.it> 1.50-6
- introduce license macro

* Tue Jun 10 2014 Alexander Kurtakov <akurtako@redhat.com> 1.50-5
- Fix FTBFS.
- Drop gcj support.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 gil cattaneo <puntogil@libero.it> 1.50-3
- add bcpkix suppport

* Tue Feb 25 2014 Michal Srb <msrb@redhat.com> - 1.50-2
- Remove unavailable dep from pom.xml

* Mon Feb 24 2014 Michal Srb <msrb@redhat.com> - 1.50-1
- Update to upstream version 1.50
- Switch to java-headless (Resolves: rhbz#1067986)
- Enable (some) tests

* Tue Oct 22 2013 gil cattaneo <puntogil@libero.it> 1.46-11
- remove versioned Jars

* Mon Aug 12 2013 gil cattaneo <puntogil@libero.it> 1.46-10
- rebuilt rhbz#995893

* Mon Aug 05 2013 gil cattaneo <puntogil@libero.it> 1.46-9
- rebuilt rhbz#992027

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-5
- use original sources from here on out

* Sat Feb 18 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-4
- Build with -source 1.6 -target 1.6

* Thu Jan 12 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-3
- Update javac target version to 1.7 to build with new java

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 01 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.46-1
- Import Bouncy Castle 1.46.
- Drop gcj.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 11 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.45-1
- Import Bouncy Castle 1.45.

* Sat Nov 14 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.44-1
- Import Bouncy Castle 1.44.

* Thu Sep 17 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-5
- Similar fixes proposed in RHBZ#521475, namely:
- Include missing properties files in jar.
- Build with javac -encoding UTF-8.
- Use %%javac and %%jar macros.
- Run test suite during build (ignoring failures for now).
- Follow upstream in excluding various test suite classes from jar.
- Add BR: junit4

* Wed Aug 26 2009 Andrew Overholt <overholt@redhat.com> 1.43-4
- Add maven POM

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-2
- Re-enable AOT bits thanks to Andrew Haley.

* Mon Apr 20 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.43-1
- Import Bouncy Castle 1.43.

* Sat Apr 18 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-4
- Rebuild

* Sat Apr 18 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-3
- Don't build AOT bits. The package needs java1.6

* Thu Apr 09 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-2
- Add missing Requires: javamail
- Remove redundant BR: junit4

* Tue Mar 17 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.42-1
- Import Bouncy Castle 1.42.
- Add javadoc subpackage.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 6 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.41-3
- Added "Provides: bcmail == %%{version}-%%{release}"
- Added "Requires: bouncycastle == %%{version}"

* Sun Oct  5 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.41-2
- Some minor fixes/improvements in the spec file
- Improved Summary/Description
- License is MIT

* Thu Oct  2 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.41-1
- Initial Release
- Spec file stolen from bouncycastle-1.41-1 and modified for bcmail
