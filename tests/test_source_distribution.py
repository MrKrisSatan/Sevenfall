"""Source provenance and shipped dependency coverage gates."""
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import release_dependencies as rd

class ReleaseDependencyTests(unittest.TestCase):
    def test_modified_source_cache_is_rejected_without_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);file=root/'source.tar.gz';file.write_bytes(b'modified')
            entry={'id':'fixture','filename':file.name,'sha256':hashlib.sha256(b'approved').hexdigest()}
            with patch.object(rd,'CACHE',root),self.assertRaisesRegex(ValueError,'checksum mismatch'):
                rd.archive(entry)
            self.assertEqual(file.read_bytes(),b'modified')

    def test_untrusted_tar_paths_cannot_escape_on_windows_or_posix(self):
        for path in ('repo/../../outside','repo/..\\outside','C:/outside','/outside'):
            buffer=io.BytesIO()
            with tarfile.open(fileobj=buffer,mode='w') as tar:
                item=tarfile.TarInfo(path);item.size=1;tar.addfile(item,io.BytesIO(b'x'))
            buffer.seek(0)
            with tarfile.open(fileobj=buffer) as tar,self.assertRaisesRegex(ValueError,'Unsafe'):
                list(rd.members(tar))

    def test_runtime_manifest_excludes_build_tools_and_project_libraries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            libs={'Audio/1.2':{'type':'package'},'Compiler/3.4':{'type':'package'},'OwnCode/1.0':{'type':'project'}}
            target={'Audio/1.2':{'native':{'sound.dll':{}}},'Compiler/3.4':{},'OwnCode/1.0':{'runtime':{'Own.dll':{}}}}
            (root/'Game.deps.json').write_text(json.dumps({'libraries':libs,'targets':{'net10.0/win-x64':target}}))
            self.assertEqual(rd.shipped_packages(root),{'audio/1.2'})
