import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from PIL import Image
from adapt import adapt,create_asset,run

class AdaptTests(unittest.TestCase):
 def test_none_is_pixel_identical_and_size_preserved(self):
  with tempfile.TemporaryDirectory() as td:
   a,b=Path(td)/'a.png',Path(td)/'b.png'; create_asset(a); adapt(a,b,[(1,2,3)],'none')
   self.assertEqual(list(Image.open(a).get_flattened_data()),list(Image.open(b).get_flattened_data()))
 def test_invalid_method_or_palette_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   a=Path(td)/'a.png'; create_asset(a)
   with self.assertRaises(ValueError): adapt(a,a,[(1,2,3)],'bad')
   with self.assertRaises(ValueError): adapt(a,a,[],'palette')
 def test_tint_preserves_transparent_pixels(self):
  with tempfile.TemporaryDirectory() as td:
   a,b=Path(td)/'alpha.png',Path(td)/'tint.png'
   im=Image.new('RGBA',(2,1),(20,30,40,255)); im.putpixel((0,0),(0,0,0,0)); im.save(a)
   adapt(a,b,[(200,100,50)],'tint')
   self.assertEqual(Image.open(b).getpixel((0,0))[3],0)
   self.assertEqual(Image.open(b).getpixel((1,0))[3],255)
 def test_run_writes_real_images_and_metrics(self):
  with tempfile.TemporaryDirectory() as td:
   r=run(Path(td)); self.assertEqual(len(r['metrics']),27); self.assertTrue((Path(td)/'palette.png').exists())
   self.assertEqual(r['asset_count'],3); self.assertEqual(r['profile_count'],3)

if __name__=='__main__': unittest.main()
