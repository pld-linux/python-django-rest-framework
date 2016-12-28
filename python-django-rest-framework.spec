# TODO
# - fix find-lang
#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module_name	rest_framework
%define		pypi_name	djangorestframework
Summary:	Web APIs for Django, made easy
Name:		python-django-rest-framework
Version:	3.4.7
Release:	2
License:	BSD
Source0:	https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	7bc1e3277cd9ad099ad5a277a2c0b433
Group:		Libraries/Python
URL:		http://www.django-rest-framework.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
Requires:	python-django
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Django REST framework is a powerful and flexible toolkit that makes it
easy to build Web APIs.

Some reasons you might want to use REST framework:
- The Web browsable API is a huge usability win for your developers.
- Authentication policies including OAuth1a and OAuth2 out of the box.
- Serialization that supports both ORM and non-ORM data sources.
- Customizable all the way down - just use regular function-based
  views if you don't need the more powerful features.
- Extensive documentation, and great community support.

%package -n python3-django-rest-framework
Summary:	Web APIs for Django, made easy
Group:		Libraries/Python
Requires:	python3-django

%description -n python3-django-rest-framework
Django REST framework is a powerful and flexible toolkit that makes it
easy to build Web APIs.

Some reasons you might want to use REST framework:
- The Web browsable API is a huge usability win for your developers.
- Authentication policies including OAuth1a and OAuth2 out of the box.
- Serialization that supports both ORM and non-ORM data sources.
- Customizable all the way down - just use regular function-based
  views if you don't need the more powerful features.
- Extensive documentation, and great community support.

%prep
%setup -q -n %{pypi_name}-%{version}

# Remove bundled egg-info
rm -r %{pypi_name}.egg-info

# remove .po files
# FIXME: why?!
find . -name *.po -exec rm -f '{}' \;

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%if 1
# find-lang doesn't work, even with --all-name
> django_py2.lang
> django_py3.lang
%else

%find_lang django

# separate into files for python2.7 and 3.x
%if %{with python2}
grep "python%{py_ver}" django.lang > django_py2.lang
%endif
%if %{with python3}
grep "python%{py3_ver}" django.lang > django_py3.lang
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files -f django_py2.lang
%defattr(644,root,root,755)
# license file is not distributed in source distribution
# https://github.com/tomchristie/django-rest-framework/issues/2906
# once it's released, license will be named LICENSE.md
#%doc LICENSE.md
%dir %{py_sitescriptdir}/rest_framework/
%{py_sitescriptdir}/rest_framework/authtoken
%dir %{py_sitescriptdir}/rest_framework/locale
%dir %{py_sitescriptdir}/rest_framework/locale/??/
%dir %{py_sitescriptdir}/rest_framework/locale/??/LC_MESSAGES
%dir %{py_sitescriptdir}/rest_framework/locale/??_??/
%dir %{py_sitescriptdir}/rest_framework/locale/??_??/LC_MESSAGES
%{py_sitescriptdir}/rest_framework/static
%{py_sitescriptdir}/rest_framework/templates
%{py_sitescriptdir}/rest_framework/templatetags
%{py_sitescriptdir}/rest_framework/utils
%{py_sitescriptdir}/rest_framework/*.py*
%{py_sitescriptdir}/%{pypi_name}-%{version}-py%{py_ver}.egg-info
%endif

%if %{with python3}
%files -n python3-django-rest-framework -f django_py3.lang
%defattr(644,root,root,755)
# license file is not distributed in source distribution
# https://github.com/tomchristie/django-rest-framework/issues/2906
#%doc LICENSE.md
%{py3_sitescriptdir}/rest_framework/__pycache__
%dir %{py3_sitescriptdir}/rest_framework/
%{py3_sitescriptdir}/rest_framework/authtoken
%dir %{py3_sitescriptdir}/rest_framework/locale
%dir %{py3_sitescriptdir}/rest_framework/locale/??/
%dir %{py3_sitescriptdir}/rest_framework/locale/??/LC_MESSAGES
%dir %{py3_sitescriptdir}/rest_framework/locale/??_??/
%dir %{py3_sitescriptdir}/rest_framework/locale/??_??/LC_MESSAGES
%{py3_sitescriptdir}/rest_framework/static
%{py3_sitescriptdir}/rest_framework/templates
%{py3_sitescriptdir}/rest_framework/templatetags
%{py3_sitescriptdir}/rest_framework/utils
%{py3_sitescriptdir}/rest_framework/*.py*
%{py3_sitescriptdir}/%{pypi_name}-%{version}-py%{py3_ver}.egg-info
%endif
