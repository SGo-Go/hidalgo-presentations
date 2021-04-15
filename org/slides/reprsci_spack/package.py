#+BEGIN_SRC python
from spack import *


class Libosrm(CMakePackage):
    """libOSRM is a high performance routing library written in C++14
    designed to run on OpenStreetMap data."""

    homepage = "http://project-osrm.org/"
    url      = "https://github.com/Project-OSRM/osrm-backend/archive/v5.24.0.tar.gz"

    maintainers = ['sgo-go']

    version('master', branch='master')
    version('5.24.0',                   sha256='a66b20e7ffe83e5e5fe12324980320e12a6ec2b05f2befd157de5c60c665613c')
    version('5.23.0-rc.2',              sha256='bc1f6024bbfd491bddaf02ac9a15fc7786274e22fd1097014a4590430fd41199')
    version('5.23.0-rc.1',              sha256='df4ad08a758be487809f477fbbdc80558c5bca3ed2a24b8719fb636a6ace8b36')
    version('5.23.0',                   sha256='8527ce7d799123a9e9e99551936821cc0025baae6f2120dbf2fbc6332c709915')
    version('5.22.0-customsnapping.3',  sha256='414922ec383f9cbfcb10f2ced80688359f1ee5e87b920b0d00b3d6eda9b5925b')
    version('5.21.0-customsnapping.11', sha256='9dcb8795ae8c581264655c818dfc2f33f394557869a738675cc41021e1c07b78')
    version('5.21.0-customsnapping.10', sha256='bbd6c3878ec559742f700e92202a7239a6c61cedfc399921f68b7d4e5eb30eb4')
    version('5.21.0-customsnapping.9',  sha256='933b6bb7b29b0f96d54814ac5d81478e0de1a05cb3f1e3d6748c941c3efc87bd')
    version('5.21.0-customsnapping.8',  sha256='ff1ac87b8671145a6dbf8d2985df07627293c939794f49b9114574f48821f2ca')
    version('5.21.0-customsnapping.7',  sha256='34562aa5ee13dd18113d926ab91147ca29677ceddec21e8e11676c51c51012a2')

    variant('shared', default=False,
            description='Enables the build of shared libraries')
    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))
    variant('osmium', default=False,
            description='Install with libosmium')
    variant('doxygen', default=False,
            description='Install with libosmium')
    variant('protozero', default=False,
            description='Install with third party Protozero (otherwise download it during installation)')

    # ---- See about OSRM library at:
    # https://github.com/Project-OSRM/osrm-backend/blob/master/docs/libosrm.md
    variant('lib_only', default=True,
            description='Install OSRM in a library only mode')
    
    # Build-time dependencies:
    # depends_on('m4', type='build') # build-essential
    depends_on('binutils', type='build')
    depends_on('pkg-config', type='build')
    depends_on('cmake@3.1:', type='build', when='@5.21:')
    depends_on('git', type='build', when='@master')

    # depends_on('expat@2.2.6:')
    depends_on('bzip2')
    depends_on('libxml2')
    depends_on('libzip')
    depends_on('zlib')
    depends_on('boost@1.54.0:')
    depends_on('lua@5.2:')
    depends_on('intel-tbb') # 2019.3

    depends_on('libosmium', when='+osmium')
    depends_on('doxygen', when='+doxygen')
    depends_on('protozero', when='+protozero')

    conflicts('%gcc', when='@:5.0', msg='libOSRM needs C++14 support (GCC >= 5)')
    # conflicts('+cxx', when='@:0.6', msg='Variant cxx requires Julia >= 1.0.0')
    # conflicts('@:0.7.0', when='target=aarch64:')
    # conflicts('@:0.5.1', when='%gcc@8:', msg='Julia <= 0.5.1 needs GCC <= 7')

    def setup_build_environment(self, env):
        env.set('LC_CTYPE', 'en_US.UTF-8')
        env.set('LC_ALL', 'en_US.UTF-8')

        env.set('BOOST_INCLUDEDIR', self.spec['boost'].headers.directories[0])
        env.set('BOOST_LIBRARYDIR', self.spec['boost'].libs.directories[0])
        
    def cmake_args(self):
        variant_bool = lambda feature: str(feature in self.spec)
        cmake_args = []

        cmake_args.append('-DLUA_INCLUDE_DIR=%s' % self.spec['lua'].headers.directories[0])
        cmake_args.append('-DBUILD_SHARED_LIBS:BOOL=%s' % variant_bool('+shared'))
        cmake_args.append('-DBoost_USE_STATIC_LIBS=ON') # %s' % variant_bool('+shared')

        return cmake_args
#+END_SRC
