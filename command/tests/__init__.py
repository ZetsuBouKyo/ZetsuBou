from pathlib import Path

from command.tests.gen.gallery import generate_galleries


class Tests:
    def _gen_tags(self):
        pass

    def _gen_simple(self, root: str):
        gallery_names = ["[中文] 安安你好 (唐詩三百首) [Chinese]", "[社會 (歷史)] 今天天氣真好 (三國演義) [Chn]"]
        img_names = [str(i) for i in range(1, 5)]
        _root = Path(root)
        generate_galleries(_root, gallery_names, img_names)

    def _gen_30010(self, root: str):
        pass

    def gen(self, root: str):
        self._gen_simple(root)

    def gen_galleries(self, root: str):
        pass

    def gen_videos(self, root: str):
        pass

    def clean(self):
        pass
