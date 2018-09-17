import unittest

import numpy as np

from chainer import testing
from chainer.testing import attr

from chainercv.datasets import coco_instance_segmentation_label_names
from chainercv.datasets import COCOInstanceSegmentationDataset
from chainercv.utils import assert_is_instance_segmentation_dataset


@testing.parameterize(*testing.product({
    'split': ['train', 'val', 'minival', 'valminusminival'],
    'use_crowded': [False, True],
    'return_crowded': [False, True],
    'return_area': [False, True]
}))
class TestCOCOInstanceSegmentationDataset(unittest.TestCase):

    def setUp(self):
        self.dataset = COCOInstanceSegmentationDataset(
            split=self.split,
            use_crowded=self.use_crowded, return_crowded=self.return_crowded,
            return_area=self.return_area)

    @attr.slow
    def test_coco_instance_segmentation_dataset(self):
        assert_is_instance_segmentation_dataset(
            self.dataset,
            len(coco_instance_segmentation_label_names),
            n_example=10)

        if self.return_area:
            for _ in range(10):
                i = np.random.randint(0, len(self.dataset))
                _, mask, _, area = self.dataset[i][:4]
                self.assertIsInstance(area, np.ndarray)
                self.assertEqual(area.dtype, np.float32)
                self.assertEqual(area.shape, (mask.shape[0],))

        if self.return_crowded:
            for _ in range(10):
                i = np.random.randint(0, len(self.dataset))
                example = self.dataset[i]
                crowded = example[-1]
                mask = example[1]
                self.assertIsInstance(crowded, np.ndarray)
                self.assertEqual(crowded.dtype, np.bool)
                self.assertEqual(crowded.shape, (mask.shape[0],))

                if not self.use_crowded:
                    np.testing.assert_equal(crowded, 0)


testing.run_module(__name__, __file__)
