'''
Created on May 14, 2014
 
@author: Furqan Wasi <furqan@avpreserve.com>
'''

messages = {}

''' Project '''
messages['in_valid_project_name'] = 'Invalid Project Name provided.  Please provide a valid project Name and try again.\nProject Name can only contain {A-z,0-9,-,_}'
messages['in_valid_project_name_detailed'] = 'Invalid project name:\n*Project names must be unique\n*Project names cannot be blank\n*Project names cannot contain spaces\n*Project names must be legal filenames.'
messages['invalid_email'] = 'Invalid email address provided.  Please provide a valid address and try again.'
messages['no_directories'] = 'No directories selected!\nPlease set directories to scan.'
messages['settings_saved'] = 'Settings saved for .'
messages['project_schedule_not_set'] = 'Project schedule not set - please select an interval for scans.'
messages['sure_delete'] = 'Are you certain that you want to delete'
messages['no_project_selected_delete'] = 'No project selected to delete - please select a project and try again.'
messages['no_project_selected'] = 'No project selected - please select a project and try again.'
messages['project_already_selected'] = 'A project with this name already exists - please enter a new project name.'
messages['project_name_changed'] = 'Project name changed successfully!'
messages['problem_proj_name_change'] = 'There was a problem changing the project name - please try again.'
messages['filter_success'] = 'Filter set successfully!'
messages['filter_fail'] = 'There was a proble while setting the filter - please try again.'
messages['not_scanned_before'] = "This project has not been scanned before, Please run the project and then try again."
messages['already_using_algorithm'] = "This Project is Already using this algorithm."
messages['algorithm_success'] = " algorithm has been changed successfully."
messages['checksum_algorithm_change_failure'] = " Checksum Algorithm Change Failure: Not all files were confirmed and the process was stopped. See report for details. Please perform the change once again to complete the process."
messages['provide_valid_pass'] = 'Please provide a password to access the reporting email account.'
messages['provide_valid_email'] = 'Invalid email address provided.  Please provide a valid address and try again'
messages['email_save_success'] = 'Credentials successfully saved!'
messages['invalid_email_given'] = 'Invalid email address provided.\nPlease provide a valid address and try again.'
messages['configure_email_pref'] = 'Please configure an email account in the Preferences menu.'
messages['got_testing_email'] = "Please check the provided email account's inbox.\nIf there is a message from Fixity, then reporting is enabled."
messages['testing_email_error'] = "Fixity was unable to send email.\n*Please ensure that you are connected to the Internet\n*Please ensure that your email credentials are correct"
messages['select_manifest_file'] = "Please select valid Project/Manifest file path"
messages['invalid_file_given'] = "Invalid File Given"
messages['project_imported_sccuessfully'] = "Project have been imported successfully"
messages['dir_dnt_exists'] = ' does not exist.\nPlease provide a valid path and try again.'

messages['project_not_ran_before'] = "This project has not been scanned before, Please run the project and then try again."
messages['alog_not_changed_mail'] = 'The process of changing the checksum algorithm requires that the all files have a status of Confirmed with the original checksum algorithm prior to updating files with the new checksum algorithm. Not all files met this criteria and the checksum change process was not completed. The report identifying the status of the verification can be found in your email or in the Fixity reports directory. Perform the operation once again to complete the process. Thanks'












''' About Fixity''' 
''' Description ''' 
messages['description_heading'] = '<h1>DESCRIPTION</h1>.'
messages['description_Content'] = '<p>AVPreserve Fixity 0.4</p> <p>Fixity was developed by AVPreserve and can be found at www.avpreserve.com/tools</p></br> <p>The GitHub repository for Fixity can be found at https://github.com/avpreserve/fixity</p> <p>Fixity is a utility for the documentation and regular review of stored files. Fixity scans a folder or directory, creating a manifest of the files including their file paths and their checksums, against which a regular comparative analysis can be run. Fixity monitors file integrity through generation and validation of checksums, and file attendance through monitoring and reporting on new, missing, moved and renamed files. Fixity emails a report to the user documenting flagged items along with the reason for a flag, such as that a file has been moved to a new location in the directory, has been edited, or has failed a checksum comparison for other reasons. Supplementing tools like BagIt that review files at points of exchange, when run regularly Fixity becomes a powerful tool for monitoring digital files in repositories, servers, and other long-term storage locations.</p>'

''' License ''' 
messages['License_heading'] = '<h1>Author and License </h1>'
messages['License_Content'] = '''<p>Fixity Copyright and License</p>
        <p>Copyright (C) 2013-2014 www.avpreserve.com, info@avpreserve.com</p></br>
        <p>Fixity is licensed under an Apache License, Version 2.0</p>
        <p>Fixity is a utility for the documentation and regular review of stored files. Fixity scans a folder or directory, creating a manifest of the files including their file paths and their checksums, against which a regular comparative analysis can be run. Fixity monitors file integrity through generation and validation of checksums, and file attendance through monitoring and reporting on new, missing, moved and renamed files. Fixity emails a report to the user documenting flagged items along with the reason for a flag, such as that a file has been moved to a new location in the directory, has been edited, or has failed a checksum comparison for other reasons. Supplementing tools like BagIt that review files at points of exchange, when run regularly Fixity becomes a powerful tool for monitoring digital files in repositories, servers, and other long-term storage locations.</p>
        <h1>Fixity License</h1></br>
        <center>Apache License</center></br>
        <center>Version 2.0, January 2004</center></br>
        <center>http://www.apache.org/licenses/</center></br>
        <p>TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION</p></br>
        <ol>
            <li>
                <p> "License" shall mean the terms and conditions for use, reproduction, and distribution as defined by Sections 1 through 9 of this document.</p>
                <p> "Licensor" shall mean the copyright owner or entity authorized by the copyright owner that is granting the License.</p>
                <p> "Legal Entity" shall mean the union of the acting entity and all other entities that control, are controlled by, or are under common control with that entity. For the purposes of this definition, "control" means (i) the power, direct or indirect, to cause the direction or management of such entity, whether by contract or otherwise, or (ii) ownership of fifty percent (50%) or more of the outstanding shares, or (iii) beneficial ownership of such entity.</p>
                <p> "You" (or "Your") shall mean an individual or Legal Entity exercising permissions granted by this License.</p>
                <p> "Source" form shall mean the preferred form for making modifications, including but not limited to software source code, documentation source, and configuration files.</p>
                <p> "Object" form shall mean any form resulting from mechanical transformation or translation of a Source form, including but not limited to compiled object code, generated documentation, and conversions to other media types.</p>
                <p> "Derivative Works" shall mean any work, whether in Source or Object form, that is based on (or derived from) the Work and for which the editorial revisions, annotations, elaborations, or other modifications represent, as a whole, an original work of authorship. For the purposes of this License, Derivative Works shall not include works that remain separable from, or merely link (or bind by name) to the interfaces of, the Work and Derivative Works thereof.</p>
                <p> "Contribution" shall mean any work of authorship, including the original version of the Work and any modifications or additions to that Work or Derivative Works thereof, that is intentionally submitted to Licensor for inclusion in the Work by the copyright owner or by an individual or Legal Entity authorized to submit on behalf of the copyright owner. For the purposes of this definition, "submitted" means any form of electronic, verbal, or written communication sent to the Licensor or its representatives, including but not limited to communication on electronic mailing lists, source code control systems, and issue tracking systems that are managed by, or on behalf of, the Licensor for the purpose of discussing and improving the Work, but excluding communication that is conspicuously marked or otherwise designated in writing by the copyright owner as "Not a Contribution."</p>
                <p> "Contributor" shall mean Licensor and any individual or Legal Entity on behalf of whom a Contribution has been received by Licensor and subsequently incorporated within the Work.</p>
            </li>
        
            <li>
                <p> Grant of Copyright License. Subject to the terms and conditions of this License, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare Derivative Works of, publicly display, publicly perform, sublicense, and distribute the Work and such Derivative Works in Source or Object form.</p>
            </li>
            <li>
                <p> Grant of Patent License. Subject to the terms and conditions of this License, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable (except as stated in this section) patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer the Work, where such license applies only to those patent claims licensable by such Contributor that are necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with the Work to which such Contribution(s) was submitted. If You institute patent litigation against any entity (including a cross-claim or counterclaim in a lawsuit) alleging that the Work or a Contribution incorporated within the Work constitutes direct or contributory patent infringement, then any patent licenses granted to You under this License for that Work shall terminate as of the date such litigation is filed.</p>
            </li>
        
            <li>
                <p> Redistribution. You may reproduce and distribute copies of the Work or Derivative Works thereof in any medium, with or without modifications, and in Source or Object form, provided that You meet the following conditions:</p>
                <ol type="a">
        
                    <li>
                        <p> You must give any other recipients of the Work or Derivative Works a copy of this License; and</p>
                    </li>
        
                    <li>
                        <p> You must cause any modified files to carry prominent notices stating that You changed the files; and</p>
                    </li>
        
                    <li>
                        <p> You must retain, in the Source form of any Derivative Works that You distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work, excluding those notices that do not pertain to any part of the Derivative Works; and</p>
                    </li>
        
                    <li>
                        <p> If the Work includes a "NOTICE" text file as part of its distribution, then any Derivative Works that You distribute must include a readable copy of the attribution notices contained within such NOTICE file, excluding those notices that do not pertain to any part of the Derivative Works, in at least one of the following places: within a NOTICE text file distributed as part of the Derivative Works; within the Source form or documentation, if provided along with the Derivative Works; or, within a display generated by the Derivative Works, if and wherever such third-party notices normally appear. The contents of the NOTICE file are for informational purposes only and do not modify the License. You may add Your own attribution notices within Derivative Works that You distribute, alongside or as an addendum to the NOTICE text from the Work, provided that such additional attribution notices cannot be construed as modifying the License.</p>
                    </li>
                </ol>
        
                <p> You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Works as a whole, provided Your use, reproduction, and distribution of the Work otherwise complies with the conditions stated in this License. </p>
        
            </li>
        
        
            <li>
                <p> Submission of Contributions. Unless You explicitly state otherwise, any Contribution intentionally submitted for inclusion in the Work by You to the Licensor shall be under the terms and conditions of this License, without any additional terms or conditions. Notwithstanding the above, nothing herein shall supersede or modify the terms of any separate license agreement you may have executed with Licensor regarding such Contributions.</p>
            </li>
        
        
            <li>
                <p> Trademarks. This License does not grant permission to use the trade names, trademarks, service marks, or product names of the Licensor, except as required for reasonable and customary use in describing the origin of the Work and reproducing the content of the NOTICE file.</p>
            </li>
        
            <li>
                <p> Disclaimer of Warranty. Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.</p>
            </li>
        
        
            <li>
                <p> Limitation of Liability. In no event and under no legal theory, whether in tort (including negligence), contract, or otherwise, unless required by applicable law (such as deliberate and grossly negligent acts) or agreed to in writing, shall any Contributor be liable to You for damages, including any direct, indirect, special, incidental, or consequential damages of any character arising as a result of this License or out of the use or inability to use the Work (including but not limited to damages for loss of goodwill, work stoppage, computer failure or malfunction, or any and all other commercial damages or losses), even if such Contributor has been advised of the possibility of such damages.</p>
            </li>
        
        
            <li>
                <p> Accepting Warranty or Additional Liability. While redistributing the Work or Derivative Works thereof, You may choose to offer, and charge a fee for, acceptance of support, warranty, indemnity, or other liability obligations and/or rights consistent with this License. However, in accepting such obligations, You may act only on Your own behalf and on Your sole responsibility, not on behalf of any other Contributor, and only if You agree to indemnify, defend, and hold each Contributor harmless for any liability incurred by, or claims asserted against, such Contributor by reason of your accepting any such warranty or additional liability.</p>
            </li> </ol> <p>END OF TERMS AND CONDITIONS</p></br> <h1>PySide License</h1></br> <p>Copyright (C) 2013 Digia Plc</p> <span>Contact: PySide team</span> <p>This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License version 2.1 as published by the Free Software Foundation. This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.</p> <p>You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA</p> <h1>SQLite License</h1></br> <p>All of the code and documentation in SQLite has been dedicated to the public domain by the authors. All code authors, and representatives of the companies they work for, have signed affidavits dedicating their contributions to the public domain and originals of those signed affidavits are stored in a firesafe at the main offices of Hwaci. Anyone is free to copy, modify, publish, use, compile, sell, or distribute the original SQLite code, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.</p><br/>'''


''' Contact Us ''' 
messages['Contact_heading'] = '<h1>Contact</h1>.'
messages['Contact_Content'] = '<p>Please post issues and feature requests at https://github.com/avpreserve/fixity/issues</p> <p>Please send questions, comments or feedback to info@avpreserve.com</p></br>'


