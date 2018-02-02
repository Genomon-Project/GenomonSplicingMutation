#! /usr/bin/env python

import unittest
import sys, os, tempfile, shutil, filecmp, tarfile
import savnet 
from check_download import *
from make_savnet_input import *

class TestMain(unittest.TestCase):

    def setUp(self):

        def extract_tar_gz(input_tar_gz_file, out_path):
            tar = tarfile.open(input_tar_gz_file)
            tar.extractall(out_path)
            tar.close()

        # prepare reference genome
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        check_download("https://storage.googleapis.com/friend1ws_package_data/common/GRCh37.fa", \
                       cur_dir + "/resource/reference_genome/GRCh37.fa")
      
        check_download("https://storage.googleapis.com/friend1ws_package_data/savnet/mutation.tar.gz", \
                       cur_dir + "/resource/mutation.tar.gz")
        extract_tar_gz(cur_dir + "/resource/mutation.tar.gz", cur_dir + "/resource")

        check_download("https://storage.googleapis.com/friend1ws_package_data/savnet/junction.tar.gz", \
                       cur_dir + "/resource/junction.tar.gz")
        extract_tar_gz(cur_dir + "/resource/junction.tar.gz", cur_dir + "/resource")

        check_download("https://storage.googleapis.com/friend1ws_package_data/savnet/intron_retention.tar.gz", \
                       cur_dir + "/resource/intron_retention.tar.gz")
        extract_tar_gz(cur_dir + "/resource/intron_retention.tar.gz", cur_dir + "/resource")

        check_download("https://storage.googleapis.com/friend1ws_package_data/savnet/qc.tar.gz", \
                       cur_dir + "/resource/qc.tar.gz")
        extract_tar_gz(cur_dir + "/resource/qc.tar.gz", cur_dir + "/resource")

        check_download("https://storage.googleapis.com/friend1ws_package_data/savnet/control.tar.gz", \
                       cur_dir + "/resource/control.tar.gz")
        extract_tar_gz(cur_dir + "/resource/control.tar.gz", cur_dir + "/resource")
 
        self.parser = savnet.parser.create_parser()

 
    def test1(self):

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        tmp_dir = tempfile.mkdtemp()

        print >> sys.stderr, "Creating sample list file for SAVNET."
        make_savnet_input(cur_dir + "/resource/savnet_input.txt", \
                          cur_dir + "/resource/mutation", \
                          cur_dir + "/resource/junction", \
                          cur_dir + "/resource/intron_retention", \
                          cur_dir + "/resource/qc")

        sample_list_file = cur_dir + "/resource/savnet_input.txt"
        output_prefix = tmp_dir + "/test"
        ref_genome = cur_dir + "/resource/reference_genome/GRCh37.fa"
        sj_control_file = cur_dir + "/resource/control/SJ_control_2_4.bed.gz"
        ir_control_file = cur_dir + "/resource/control/IR_control_4.bed.gz"

        print >> sys.stderr, "Executing SAVNET."
        args = self.parser.parse_args([sample_list_file, output_prefix, ref_genome, \
                                       "--SJ_pooled_control_file", sj_control_file, \
                                       "--IR_pooled_control_file", ir_control_file, "--grc"])
        savnet.run.savnet_main(args)

        self.assertTrue(394 <= len(open(tmp_dir + "/test.savnet.result.txt", 'r').readlines()) <= 404)
        shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    unittest.main()
