Generate histograms about your solar power from pijuice data.

## Build

This project can be built as a debian package using the provided [Dockerfile](Dockerfile). If you have
`docker` and `make` installed, only thing you need to do is to run:

```bash
make
```

The details of the deb package build process are explained [here](https://opensource.com/article/20/4/package-python-applications-linux).

### Add new entry to changelog
Using [dch](https://manpages.debian.org/jessie/devscripts/dch.1.en.html):

`dch -i`

Don't forget to have set your 

## License

Distributed under the MIT License. See [LICENSE.txt](LICENSE.txt) for more information.
