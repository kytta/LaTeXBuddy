#!/bin/bash
declare -A osInfo;
osInfo[/etc/debian_version]="apt-get install -y"
osInfo[/etc/alpine-release]="apk --update add"
osInfo[/etc/centos-release]="yum install -y"
osInfo[/etc/fedora-release]="dnf install -y"
osInfo[/etc/redhat-release]="yum install -y"
osInfo[/etc/arch-release]="pacman -U"
osInfo[/etc/gentoo-release]="emerge"
osInfo[/etc/SuSE-release]="zypper install -y"
packages=(python3-pip git default-jdk curl make)

for f in ${!osInfo[@]}
do
    if [[ -f $f ]];then
        package_manager=${osInfo[$f]}
    fi
done

for i in ${packages[@]}
do
    if [[ $package_manager == "apt-get" ]]; then
        update="apt-get update -y"
        ${update}
    fi
    ${package_manager} ${i}
done

TPATH=$HOME/chktex-1.7.6.tar.gz
FPATH=$HOME/chktex
TAR='/usr/bin/tar'
url='http://download.savannah.gnu.org/releases/chktex/chktex-1.7.6.tar.gz'
curl -L $url > TPATH
tar -xvf TPATH -C $FPATH


TARPATH=$HOME/diction-1.14.tar.gz
FPATH=$HOME/diction
url=http://ftp.gnu.org/gnu/diction/diction-1.11.tar.gz
curl $url > $TARPATH

TARPATH=$HOME/LanguageTool-5.3.zip
FPATH=$HOME/languageTool
url=https://languagetool.org/download/LanguageTool-5.3.zip
curl $url > $TARPATH

TARPATH=$HOME/aspell-master.zip
FPATH=$HOME/aspell
url=https://github.com/GNUAspell/aspell/aspell-master.zip
curl $url > $TARPATH

TARPATH=$HOME/latexbuddy-master.tar.gz
FPATH=$HOME/latexbuddy
url=https://git.rz.tu-bs.de/sw-technik-fahrzeuginformatik/sep/sep-2021/ibr_alg_0/latexbuddy/latexbuddy-master.tar.gz
curl $url > $TARPATH
