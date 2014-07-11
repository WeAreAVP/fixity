# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''

# built-in libraries
import os
import random
import shutil

# Custom libraries
import sys
base_path = os.getcwd()
base_path = base_path.replace(r'\test', '')
base_path = base_path.replace(r'\Fixture', '')
sys.path.append(base_path+os.sep)
import Main


class Fixtures(object):


    def __init__(self):
        self.App = Main.Main()

        self.unit_test_folder = self.App.Fixity.Configuration.getUnit_test_folder()
        self.unit_test_folder_special = self.App.Fixity.Configuration.getUnit_test_folder_special()

        self.project_name = 'New_Project'
        self.test_file_one = self.unit_test_folder + '1.docx'
        self.test_file_two = self.unit_test_folder + '2.docx'
        self.test_file_three = self.unit_test_folder + '3.docx'
        self.test_file_four = self.unit_test_folder + '4.txt'

        self.test_file_one_special = self.unit_test_folder_special +\
        '¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ.shpÿ1.docx'

        self.test_file_two_special = self.unit_test_folder_special +\
        '¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ.shpÿ2.docx'

        self.test_file_three_special = self.unit_test_folder_special + \
        '¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ.shpÿ3.docx'

        self.test_file_four_special = self.unit_test_folder_special +\
        'Unidade_de_C@.#$%onservação4.txt'

        self.test_history_file = self.unit_test_folder + 'history.tsv'
        self.attachment = self.unit_test_folder + 'attachment.tsv'
        pass


    def delete_testing_data(self):
        """
        Delete Testing Data For Unit Test
        """
        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)
        try:
            if os.path.exists(self.unit_test_folder_special.decode('utf-8')):
                try:
                    shutil.rmtree(self.unit_test_folder_special.decode('utf-8'))
                except:
                    pass
        except:
            if os.path.exists(self.unit_test_folder_special):
                shutil.rmtree(self.unit_test_folder_special)
            pass

        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableProject, '1 = 1')
        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableVersionDetail, '1 = 1')
        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableProjectPath, '1 = 1')

        self.unload_verification_algorithm_data()
        self.unload_verification_algorithm_data_special()
        pass

    def load_verification_algorithm_data(self):
        """
        Load Verification Algorithm Data For Unit Test
        """
        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)
        os.makedirs(self.unit_test_folder)

        file_obj1 = open(self.test_file_one, 'w+')
        file_obj1.write('1 document')
        file_obj1.close()

        file_obj1 = open(self.test_file_two, 'w+')
        file_obj1.write('2 document')
        file_obj1.close()

        file_obj1 = open(self.test_file_three, 'w+')
        file_obj1.write('3 document')
        file_obj1.close()

        file_obj1 = open(self.test_file_four, 'w+')
        file_obj1.write('4 document')
        file_obj1.close()


    def load_special_verification_algorithm_data(self):
        """
        Load Verification Algorithm Data For Unit Test
        """
        if os.path.exists(self.unit_test_folder_special.decode('utf-8')):
            shutil.rmtree(self.unit_test_folder_special.decode('utf-8'))
        os.makedirs(self.unit_test_folder_special.decode('utf-8'))

        file_obj1 = open(self.test_file_one_special.decode('utf-8'), 'w+')
        file_obj1.write('1 document' + str(random.randrange(1, 10000)))
        file_obj1.close()

        file_obj1 = open(self.test_file_two_special.decode('utf-8'), 'w+')
        file_obj1.write('2 document' + str(random.randrange(1, 10000)))
        file_obj1.close()

        file_obj1 = open(self.test_file_three_special.decode('utf-8'), 'w+')
        file_obj1.write('3 document' + str(random.randrange(1, 10000)))
        file_obj1.close()

        file_obj1 = open(self.test_file_four_special.decode('utf-8'), 'w+')
        file_obj1.write('4 document')
        file_obj1.close()

    def load_history_file(self):
        """
        Load History File For Unit Test
        """
        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)
        os.makedirs(self.unit_test_folder)

        test_history_file = open(self.test_history_file, 'w+')
        history_content = [
        r"d:\python\Fixity Project\test\test\;" + "\n",
        "\n"
        "99  0 99\n",
        "2014-07-02 13:32:56\n",
        "||-||1\n",
        "sha256\n",
        r"de5450da6769fe7dc515439c235d92ca34b2f979e68ed5e97931fd9ad568fbfa	d:\python\Fixity Project\test\test\\1.docx	3803196084131072658628" + "\n",
        r"83426e9311b5942db5d3f55eb17dd00238f9def3aaa819949bc653bb595e1b08	d:\python\Fixity Project\test\test\\2.docx	3803196084131072658629" + "\n",
        r"412eec9d4443bc26ae1e61c373e9768d44babf7d838d61cfd34e59647b88fa74	d:\python\Fixity Project\test\test\\3.docx	3803196084131072658630" + "\n"]

        test_history_file.writelines(history_content)
        test_history_file.close()

    def load_attachment(self):
        """
        Load Attachments For Unit Test
        """
        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)

        os.makedirs(self.unit_test_folder)

        attachment_file_obj = open(self.attachment, 'w+')
        attachment_file_obj.write('Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment Testing Attachment ')
        attachment_file_obj.close()

    def unload_attachment(self):
        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)

    def unload_verification_algorithm_data(self):
        """
        Delete Testing Data For Unit Test
        """

        if os.path.exists(self.unit_test_folder):
            shutil.rmtree(self.unit_test_folder)

        try:
            testing_new_dir = self.App.Fixity.Configuration.getBasePath()+'test3'
            if os.path.exists(testing_new_dir):
                shutil.rmtree(testing_new_dir)
        except:
            pass

        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableVersionDetail, '1 = 1')
        pass

    def unload_verification_algorithm_data_special(self):
        """
        Unload Verification Algorithm Data Special For Unit Test
        """
        if os.path.exists(self.unit_test_folder_special):
            shutil.rmtree(self.unit_test_folder_special)

        self.App.Fixity.Database.delete(self.App.Fixity.Database._tableVersionDetail, '1 = 1')
        pass