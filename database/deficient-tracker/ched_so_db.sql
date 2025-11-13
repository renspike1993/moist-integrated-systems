-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 18, 2025 at 10:45 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ched_so_db`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetDocumentsByProgramId` (IN `prog_id` VARCHAR(10))   BEGIN
    SELECT 
        d.doc_id,
        d.doc_name,
        d.required_for,
        d.purpose,
        d.prevalence,
        pd.program_id,
        pd.major,
        pd.notes
    FROM 
        documents d
    INNER JOIN 
        program_documents pd ON d.doc_id = pd.doc_id
    INNER JOIN 
        programs p ON pd.program_id = p.program_id
    WHERE 
        p.program_id = prog_id;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `applicant`
--

CREATE TABLE `applicant` (
  `fullname` varchar(255) NOT NULL,
  `program_id` varchar(10) NOT NULL,
  `major` varchar(255) DEFAULT NULL,
  `contact_number` varchar(15) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `batch_id` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applicant`
--

INSERT INTO `applicant` (`fullname`, `program_id`, `major`, `contact_number`, `email`, `batch_id`, `id`) VALUES
('Mary Ann Mae Macas', 'BSIT', NULL, '0967-258-6890', 'cold.renspike@gmail.com', 6, 1),
('Rene M. Cabuhan II', 'BSIT', 'None2', '09672586890', 'asddasdasd@gmail.com', NULL, 3),
('asdasda', 'BSIT', NULL, 'asd', 'asddasdasd@gmail.com', 6, 5),
('Melan Zaballero', 'BSIT', NULL, 'asd', 'asddasdasd@gmail.com', NULL, 6),
('Budlao Jomarie\r\n', 'BSIT', NULL, 'asd', 'asddasdasd@gmail.com', NULL, 7),
('Rene M. Cabuhan IIasd', 'BSIT', 'None2', '09672586890', 'asddasdasd@gmail.com', NULL, 9),
('asdasdaasdasd', 'BSIT', NULL, 'asd', 'asddasdasd@gmail.com', NULL, 10),
('Melan Zaballeroasdas', 'BSIT', NULL, 'asd', 'asddasdasd@gmail.com', NULL, 11),
('Budlao Jomarie\r\nasdasd', 'BSIT', NULL, 'asd', 'asddasdasd@gmail.com', NULL, 12),
('Budlao Jomarie\r\nasdasd asdas', 'BSIT', NULL, 'asd', 'asddasdasd@gmail.com', 6, 13),
('Rene Macabecha Cabuhan III', 'BSIT', 'None', '09672586890', 'cold.renspike@gmail.com', NULL, 14),
('Kennedy Elequin', 'BSIT', 'None', '99999999999', 'admin@moist.com', NULL, 15),
('Keith', 'BSIT', 'None', '0000000000', 'casd@asd', NULL, 16);

-- --------------------------------------------------------

--
-- Table structure for table `applicant_deficiencies`
--

CREATE TABLE `applicant_deficiencies` (
  `deficiencies_id` int(11) NOT NULL,
  `applicant_id` int(11) NOT NULL,
  `excuse` varchar(512) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applicant_deficiencies`
--

INSERT INTO `applicant_deficiencies` (`deficiencies_id`, `applicant_id`, `excuse`, `id`) VALUES
(11, 1, NULL, 44),
(7, 16, NULL, 45);

-- --------------------------------------------------------

--
-- Table structure for table `batch`
--

CREATE TABLE `batch` (
  `program_id` varchar(11) NOT NULL,
  `date_of_graduation` date NOT NULL,
  `deficiency_recommendation` text NOT NULL,
  `deficiency_compliance` text NOT NULL,
  `deficiency_date` date NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `batch`
--

INSERT INTO `batch` (`program_id`, `date_of_graduation`, `deficiency_recommendation`, `deficiency_compliance`, `deficiency_date`, `id`) VALUES
('BSBA', '2025-06-18', 'asdas', 'aasdsadasda asdasdasd', '2025-06-17', 6),
('BSBA', '2025-06-23', 'asdsad', 'asdasdasdsa', '0000-00-00', 7);

-- --------------------------------------------------------

--
-- Table structure for table `deficiencies`
--

CREATE TABLE `deficiencies` (
  `id` int(11) NOT NULL,
  `doc_id` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `acceptable_excuse` varchar(512) DEFAULT NULL,
  `probable_excuse` varchar(512) DEFAULT NULL,
  `common_excuse` varchar(512) DEFAULT NULL,
  `prevalence` varchar(512) DEFAULT NULL,
  `severity` varchar(512) DEFAULT NULL,
  `resolution_statement` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `deficiencies`
--

INSERT INTO `deficiencies` (`id`, `doc_id`, `description`, `acceptable_excuse`, `probable_excuse`, `common_excuse`, `prevalence`, `severity`, `resolution_statement`) VALUES
(1, 1, 'Missing notary public seal/signature', 'The notary was unavailable on the submission day.', 'Submitted a draft copy by mistake.', 'Thought the scanned file already had the seal.', '⭐⭐⭐⭐', 'Critical', 'Re-submit the form with the proper notarization from a licensed notary.'),
(2, 1, 'Incomplete applicant details', 'Applicant had pending legal name correction.', 'Rushed submission due to deadline pressure.', 'Forgot to double-check the form before uploading.', '⭐⭐⭐⭐', 'High', 'Complete all missing details and submit a fully filled, notarized version.'),
(3, 1, 'Wrong CHED form version used', 'School issued the old version unknowingly.', 'Confusion between CHED updates.', 'Downloaded the first form found online.', '⭐⭐⭐⭐', 'High', 'Replace with the current CHED form version and notarize appropriately.'),
(4, 2, 'Outdated curriculum (not CHED-endorsed)', 'CHED update was not yet released to the institution.', 'The department was still transitioning to the new version.', 'Used the last available file version.', '⭐⭐⭐⭐⭐', 'Critical', 'Secure and submit the updated CHED-approved curriculum.'),
(5, 2, 'Curriculum mismatch with applied program', 'Cross-applied to a closely related program.', 'Accidentally submitted curriculum from a similar track.', 'Miscommunication between applicant and academic advisor.', '⭐⭐⭐⭐⭐', 'Critical', 'Re-submit the correct curriculum for the applied program.'),
(6, 2, 'Missing CHED stamp', 'The stamp was forgotten during printing.', 'Scanned copy lacked the original page with the stamp.', 'The stamp page was uploaded separately.', '⭐⭐⭐⭐⭐', 'Critical', 'Attach the page with the CHED stamp or request a verified copy from the registrar.'),
(7, 3, 'Incomplete subjects/units', 'Some grades were pending encoding.', 'Registrar was still processing final grades.', 'Updates were not yet reflected in the database.', '⭐⭐⭐⭐', 'High', 'Submit an updated Form 9 with all completed subjects and units.'),
(8, 3, 'No registrar’s signature/dry seal', 'Final validation was not completed before submission.', 'Dry seal machine was unavailable during printing.', 'Scanned version was from an earlier draft.', '⭐⭐⭐⭐', 'Critical', 'Have the registrar sign and affix the dry seal to authenticate the document.'),
(9, 3, 'Discrepancy against Transcript of Records (TOR)', 'Subject codes differed between forms.', 'One record had outdated naming conventions.', 'Grades were updated after TOR was printed.', '⭐⭐⭐⭐', 'High', 'Ensure synchronization of records and submit corrected versions.'),
(10, 4, 'Uncertified copy, no stamp of \"Certified True Copy\"', 'Printed in haste without final certification.', 'Certification step was skipped accidentally.', 'Document was assumed to be already certified.', '⭐⭐⭐⭐⭐', 'Critical', 'Obtain and submit a certified true copy with official markings.'),
(11, 4, 'Missing pages', 'Page count was miscalculated before scanning.', 'Middle pages were left out by mistake.', 'Document was too large and split into separate files.', '⭐⭐⭐⭐⭐', 'Critical', 'Combine all pages into one certified copy and re-submit.'),
(12, 4, 'Name mismatch vs. PSA birth certificate', 'Legal name change was recently processed.', 'Old school records used former name format.', 'PSA update not yet reflected in school database.', '⭐⭐⭐⭐⭐', 'High', 'Submit supporting documents (e.g., affidavit or corrected PSA) for name reconciliation.'),
(13, 5, 'Unsigned by school head/registrar', 'Signer was on leave during processing.', 'Template used lacked signature fields.', 'Signature was scheduled for final batch but delayed.', '⭐⭐⭐', 'Critical', 'Request re-issuance with all official signatures.'),
(14, 5, 'Incorrect program title', 'Program title changed recently at the school.', 'Template used the legacy title.', 'Editing error during document preparation.', '⭐⭐⭐', 'High', 'Request correction and reprinting with the accurate program title.'),
(15, 5, 'Graduation date mismatch with TOR', 'Clerical encoding error between departments.', 'Graduation date was changed after final grades.', 'One document reflected the completion date, the other the ceremony.', '⭐⭐⭐', 'High', 'Align graduation records and request corrected documents.'),
(16, 6, 'Not using CHED’s template', 'School used internal evaluation version.', 'Unaware of updated CHED format.', 'Template source was outdated.', '⭐⭐⭐', 'Medium', 'Reformat the evaluation using the standard CHED template.'),
(17, 6, 'No evaluator signature', 'Evaluator was off-duty when printed.', 'Signature page was uploaded separately.', 'Form was rushed for deadline compliance.', '⭐⭐⭐', 'High', 'Request evaluator to sign and submit updated copy.'),
(18, 6, 'Math errors in unit calculations', 'Manual computation without digital checker.', 'Last-minute changes affected totals.', 'Template formula didn’t auto-update.', '⭐⭐⭐', 'Medium', 'Review, recalculate, and submit corrected evaluation.'),
(19, 7, 'Insufficient hours logged', 'Final logs weren’t consolidated in time.', 'Company HR missed the last update.', 'Logbook pages were submitted separately.', '⭐⭐⭐⭐', 'Critical', 'Complete logs, validate with supervisor, and resubmit certificate.'),
(20, 7, 'Missing company supervisor signature', 'Supervisor resigned before sign-off.', 'Signature page was left blank unintentionally.', 'Digital signature was not recognized by CHED.', '⭐⭐⭐⭐', 'High', 'Return to the company and have the supervisor sign the document.'),
(21, 7, 'No official letterhead', 'Company had no template with header.', 'Used draft version of the certificate.', 'Header printing was missed in PDF export.', '⭐⭐⭐⭐', 'Medium', 'Request reprinting on official company letterhead.'),
(22, 8, 'Outdated form version', 'Form was pulled from old archive link.', 'CHEDRO staff gave the earlier template.', 'Updated version was released post-submission.', '⭐⭐⭐', 'Medium', 'Replace with the latest CHEDRO form from official sources.'),
(23, 8, 'Missing regional office stamp', 'Regional officer was unavailable.', 'Stamp was intended for the physical copy only.', 'Digital submission didn’t require it previously.', '⭐⭐⭐', 'High', 'Visit CHEDRO and request proper stamping of the form.'),
(24, 8, 'Unchecked document checklist boxes', 'Applicant thought checklist was optional.', 'Overlooked page during form filling.', 'Boxes didn’t appear properly on printed copy.', '⭐⭐⭐', 'Medium', 'Re-submit the form with all required boxes checked.'),
(25, 9, 'Illegible scan', 'Low-resolution scanner used at barangay office.', 'Image compressed during email transfer.', 'Photocopied version was scanned instead of original.', '⭐⭐⭐⭐', 'Medium', 'Submit a high-resolution certified copy from PSA.'),
(26, 9, 'Middle name/suffix discrepancies', 'Name variations exist across documents.', 'Suffix was omitted in one official entry.', 'PSA record was updated but not yet received.', '⭐⭐⭐⭐', 'High', 'Submit an affidavit or secondary documents for clarification.'),
(27, 9, 'Uncertified copy', 'Printed version was taken from online preview.', 'Certificate copy was missing dry seal.', 'Certified version was requested but delayed.', '⭐⭐⭐⭐', 'Critical', 'Secure and submit an official PSA-certified document.'),
(28, 10, 'Validity expired (>6 months old)', 'Applicant reused old document from a previous application.', 'Was unaware of 6-month rule.', 'School issued the document earlier than expected.', '⭐⭐', 'Medium', 'Request an updated certificate with a current date.'),
(29, 10, 'No school seal', 'Seal stamping process was not yet complete.', 'Digital version skipped seal page.', 'School staff forgot to include the page.', '⭐⭐', 'High', 'Visit the school and request resealing.'),
(30, 10, 'Generic unsigned template', 'Used as placeholder pending official copy.', 'Signed version was scanned separately.', 'Applicant submitted wrong file.', '⭐⭐', 'Medium', 'Get the final signed and sealed copy from the school.'),
(31, 11, 'Payment for wrong program/region', 'Payment portal auto-selected incorrect region.', 'Manual encoding error in transaction note.', 'Similar account code confused the payer.', '⭐⭐⭐', 'High', 'Request refund and pay again under the correct details.'),
(32, 11, 'Screenshot (not official receipt)', 'Applicant thought screenshot was valid.', 'E-receipt wasn’t generated by system at the time.', 'Used mobile payment platform without receipt export.', '⭐⭐⭐', 'Medium', 'Submit an official receipt or transaction slip.'),
(33, 11, 'Name mismatch', 'Payment was done by a relative.', 'Used maiden name during transaction.', 'Auto-filled account used different name.', '⭐⭐⭐', 'High', 'Attach a signed explanation and valid ID of payer.'),
(34, 12, 'Incorrect size/background color', 'Followed generic passport photo rules.', 'Photographer wasn’t informed of CHED specs.', 'Template photo had default white background.', '⭐⭐', 'Low', 'Retake photo following official guidelines.'),
(35, 12, 'Low resolution/blurry', 'Taken with a basic phone camera.', 'File compressed during upload.', 'Reprint scan reduced quality.', '⭐⭐', 'Medium', 'Submit a clear, high-resolution photo taken professionally.'),
(36, 12, 'Digital alterations (filters)', 'Applied auto-enhance during editing.', 'Used a photo app with default filters.', 'Brightness adjusted for visibility.', '⭐⭐', 'Medium', 'Submit an unedited photo that meets CHED photo standards.'),
(37, 13, 'Missing lesson plans in portfolio', 'Plans were submitted separately.', 'Lesson files got corrupted during upload.', 'Forgot to include lesson plans folder.', '⭐⭐⭐', 'Medium', 'Merge all parts of the portfolio and re-upload complete file.'),
(38, 13, 'No supervising teacher evaluations', 'Teacher was on leave during finalization.', 'Evaluation form was misplaced.', 'Was pending approval during deadline.', '⭐⭐⭐', 'High', 'Follow up with supervisor and attach signed evaluations.'),
(39, 14, 'Incomplete review hours', 'Missed a few sessions due to illness.', 'Review center did not include all dates.', 'Certificate only reflected core hours.', '⭐⭐', 'Medium', 'Enroll in make-up sessions or submit a justification.'),
(40, 14, 'Uncertified certificate', 'Issued copy was a draft.', 'Original certification was scheduled later.', 'Scanned file had no official marks.', '⭐⭐', 'High', 'Request official hard copy with seal and signature.'),
(41, 15, 'Insufficient delivery attendance records', 'Attendance tracking was inconsistent.', 'Rotation schedule was incomplete.', 'Logbook entries were submitted late.', '⭐⭐⭐⭐', 'Critical', 'Request validation and certified log reconstruction from the hospital.'),
(42, 15, 'Missing hospital supervisor signature', 'Supervisor was off-duty during signing.', 'Signature page was not uploaded.', 'Digital form lost during system update.', '⭐⭐⭐⭐', 'Critical', 'Contact hospital to obtain signature or request re-issuance.'),
(43, 16, 'Expired eligibility certificate', 'Reused old certificate unknowingly.', 'Thought eligibility didn’t expire.', 'Certificate was valid at application time.', '⭐⭐⭐', 'High', 'Request updated certificate or renew eligibility.'),
(44, 16, 'Name mismatch with academic records', 'Used middle initial in PRC record only.', 'Name was changed after graduation.', 'Encoding error during PRC application.', '⭐⭐⭐', 'High', 'Submit affidavit of discrepancy or request a corrected certificate.');

-- --------------------------------------------------------

--
-- Table structure for table `documents`
--

CREATE TABLE `documents` (
  `doc_id` int(11) NOT NULL,
  `doc_name` varchar(100) NOT NULL,
  `required_for` varchar(50) NOT NULL,
  `purpose` text DEFAULT NULL,
  `prevalence` enum('⭐','⭐⭐','⭐⭐⭐','⭐⭐⭐⭐','⭐⭐⭐⭐⭐') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `documents`
--

INSERT INTO `documents` (`doc_id`, `doc_name`, `required_for`, `purpose`, `prevalence`) VALUES
(1, 'Notarized Application Form', 'All applicants', 'Formal request for CHED issuance', '⭐⭐⭐⭐'),
(2, 'CHED-Approved Curriculum', 'All programs', 'Basis for academic compliance check', '⭐⭐⭐⭐⭐'),
(3, 'Form IX', 'All programs', 'Academic summary for completion verification', '⭐⭐⭐⭐'),
(4, 'Transcript of Records', 'All programs', 'Primary proof of academic records', '⭐⭐⭐⭐⭐'),
(5, 'Diploma/Certificate of Graduation', 'All programs', 'Evidence of program completion', '⭐⭐⭐'),
(6, 'Evaluation Sheet', 'All programs', 'Course-by-course validation tool', '⭐⭐⭐'),
(7, 'Certificate of Completion/OJT/Practicum', 'Skills-based programs', 'Validates internship requirements', '⭐⭐⭐⭐'),
(8, 'CHEDRO Endorsement Form', 'All applicants', 'For CHED Regional Office routing', '⭐⭐⭐'),
(9, 'PSA Birth/Marriage Certificate', 'Name change cases', 'Confirms identity details', '⭐⭐⭐⭐'),
(10, 'Good Moral Character Certificate', 'All applicants', 'Character clearance', '⭐⭐'),
(11, 'Proof of Payment', 'All applicants', 'Verifies fee compliance', '⭐⭐⭐'),
(12, '2x2 ID Photo', 'All applicants', 'For CHED records', '⭐⭐'),
(13, 'Teaching Internship Portfolio', 'Education programs', 'Documentation of teaching practice', '⭐⭐⭐'),
(14, 'LET Review Certificate', 'Education programs', 'Proof of board exam preparation', '⭐⭐'),
(15, 'Clinical Training Record', 'Midwifery', 'Documentation of clinical hours', '⭐⭐⭐⭐'),
(16, 'PRC Board Eligibility Cert', 'Midwifery', 'Proof of board eligibility', '⭐⭐⭐');

-- --------------------------------------------------------

--
-- Table structure for table `programs`
--

CREATE TABLE `programs` (
  `program_id` varchar(10) NOT NULL,
  `program_name` varchar(100) NOT NULL,
  `ojt_hours_required` int(11) DEFAULT NULL,
  `major` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `programs`
--

INSERT INTO `programs` (`program_id`, `program_name`, `ojt_hours_required`, `major`) VALUES
('BEEd', 'Bachelor of Elementary Education', 600, ''),
('BSBA', 'Bachelor of Science in Business Administration', 400, 'Financial Management'),
('BSBA', 'Bachelor of Science in Business Administration', 400, 'Human Resource'),
('BSBA', 'Bachelor of Science in Business Administration', 400, 'Marketing'),
('BSBA', 'Bachelor of Science in Business Administration', 400, 'Operations'),
('BSCrim', 'Bachelor of Science in Criminology', 600, ''),
('BSED', 'Bachelor of Secondary Education', 600, 'English'),
('BSED', 'Bachelor of Secondary Education', 600, 'Mathematics'),
('BSED', 'Bachelor of Secondary Education', 600, 'Social Studies'),
('BSED', 'Bachelor of Secondary Education', 600, 'Values Education'),
('BSHM', 'Bachelor of Science in Hospitality Management', 500, ''),
('BSIT', 'Bachelor of Science in Information Technology', 486, ''),
('BSOA', 'Bachelor of Science in Office Administration', 400, ''),
('BSTM', 'Bachelor of Science in Tourism Management', 500, ''),
('Midwifery', 'Bachelor of Science in Midwifery', 800, '');

-- --------------------------------------------------------

--
-- Table structure for table `program_documents`
--

CREATE TABLE `program_documents` (
  `program_id` varchar(10) NOT NULL,
  `major` varchar(50) NOT NULL,
  `doc_id` int(11) NOT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `program_documents`
--

INSERT INTO `program_documents` (`program_id`, `major`, `doc_id`, `notes`) VALUES
('BEEd', '', 1, 'Required for all programs'),
('BEEd', '', 2, 'Required for all programs'),
('BEEd', '', 3, 'Required for all programs'),
('BEEd', '', 4, 'Required for all programs'),
('BEEd', '', 5, 'Required for all programs'),
('BEEd', '', 6, 'Required for all programs'),
('BEEd', '', 7, 'Minimum 600 hours'),
('BEEd', '', 8, 'Required for all programs'),
('BEEd', '', 9, 'Required for all programs'),
('BEEd', '', 10, 'Required for all programs'),
('BEEd', '', 11, 'Required for all programs'),
('BEEd', '', 12, 'Required for all programs'),
('BEEd', '', 13, 'Required for Education programs'),
('BEEd', '', 14, 'Required for Education programs'),
('BSBA', 'Financial Management', 1, 'Required for all programs'),
('BSBA', 'Financial Management', 2, 'Required for all programs'),
('BSBA', 'Financial Management', 3, 'Required for all programs'),
('BSBA', 'Financial Management', 4, 'Required for all programs'),
('BSBA', 'Financial Management', 5, 'Required for all programs'),
('BSBA', 'Financial Management', 6, 'Required for all programs'),
('BSBA', 'Financial Management', 7, 'Minimum 400 hours'),
('BSBA', 'Financial Management', 8, 'Required for all programs'),
('BSBA', 'Financial Management', 9, 'Required for all programs'),
('BSBA', 'Financial Management', 10, 'Required for all programs'),
('BSBA', 'Financial Management', 11, 'Required for all programs'),
('BSBA', 'Financial Management', 12, 'Required for all programs'),
('BSBA', 'Human Resource', 1, 'Required for all programs'),
('BSBA', 'Human Resource', 2, 'Required for all programs'),
('BSBA', 'Human Resource', 3, 'Required for all programs'),
('BSBA', 'Human Resource', 4, 'Required for all programs'),
('BSBA', 'Human Resource', 5, 'Required for all programs'),
('BSBA', 'Human Resource', 6, 'Required for all programs'),
('BSBA', 'Human Resource', 7, 'Minimum 400 hours'),
('BSBA', 'Human Resource', 8, 'Required for all programs'),
('BSBA', 'Human Resource', 9, 'Required for all programs'),
('BSBA', 'Human Resource', 10, 'Required for all programs'),
('BSBA', 'Human Resource', 11, 'Required for all programs'),
('BSBA', 'Human Resource', 12, 'Required for all programs'),
('BSBA', 'Marketing', 1, 'Required for all programs'),
('BSBA', 'Marketing', 2, 'Required for all programs'),
('BSBA', 'Marketing', 3, 'Required for all programs'),
('BSBA', 'Marketing', 4, 'Required for all programs'),
('BSBA', 'Marketing', 5, 'Required for all programs'),
('BSBA', 'Marketing', 6, 'Required for all programs'),
('BSBA', 'Marketing', 7, 'Minimum 400 hours'),
('BSBA', 'Marketing', 8, 'Required for all programs'),
('BSBA', 'Marketing', 9, 'Required for all programs'),
('BSBA', 'Marketing', 10, 'Required for all programs'),
('BSBA', 'Marketing', 11, 'Required for all programs'),
('BSBA', 'Marketing', 12, 'Required for all programs'),
('BSBA', 'Operations', 1, 'Required for all programs'),
('BSBA', 'Operations', 2, 'Required for all programs'),
('BSBA', 'Operations', 3, 'Required for all programs'),
('BSBA', 'Operations', 4, 'Required for all programs'),
('BSBA', 'Operations', 5, 'Required for all programs'),
('BSBA', 'Operations', 6, 'Required for all programs'),
('BSBA', 'Operations', 7, 'Minimum 400 hours'),
('BSBA', 'Operations', 8, 'Required for all programs'),
('BSBA', 'Operations', 9, 'Required for all programs'),
('BSBA', 'Operations', 10, 'Required for all programs'),
('BSBA', 'Operations', 11, 'Required for all programs'),
('BSBA', 'Operations', 12, 'Required for all programs'),
('BSCrim', '', 1, 'Required for all programs'),
('BSCrim', '', 2, 'Required for all programs'),
('BSCrim', '', 3, 'Required for all programs'),
('BSCrim', '', 4, 'Required for all programs'),
('BSCrim', '', 5, 'Required for all programs'),
('BSCrim', '', 6, 'Required for all programs'),
('BSCrim', '', 7, 'Minimum 600 hours'),
('BSCrim', '', 8, 'Required for all programs'),
('BSCrim', '', 9, 'Required for all programs'),
('BSCrim', '', 10, 'Required for all programs'),
('BSCrim', '', 11, 'Required for all programs'),
('BSCrim', '', 12, 'Required for all programs'),
('BSED', 'English', 1, 'Required for all programs'),
('BSED', 'English', 2, 'Required for all programs'),
('BSED', 'English', 3, 'Required for all programs'),
('BSED', 'English', 4, 'Required for all programs'),
('BSED', 'English', 5, 'Required for all programs'),
('BSED', 'English', 6, 'Required for all programs'),
('BSED', 'English', 7, 'Minimum 600 hours'),
('BSED', 'English', 8, 'Required for all programs'),
('BSED', 'English', 9, 'Required for all programs'),
('BSED', 'English', 10, 'Required for all programs'),
('BSED', 'English', 11, 'Required for all programs'),
('BSED', 'English', 12, 'Required for all programs'),
('BSED', 'English', 13, 'Required for Education programs'),
('BSED', 'English', 14, 'Required for Education programs'),
('BSED', 'Mathematics', 1, 'Required for all programs'),
('BSED', 'Mathematics', 2, 'Required for all programs'),
('BSED', 'Mathematics', 3, 'Required for all programs'),
('BSED', 'Mathematics', 4, 'Required for all programs'),
('BSED', 'Mathematics', 5, 'Required for all programs'),
('BSED', 'Mathematics', 6, 'Required for all programs'),
('BSED', 'Mathematics', 7, 'Minimum 600 hours'),
('BSED', 'Mathematics', 8, 'Required for all programs'),
('BSED', 'Mathematics', 9, 'Required for all programs'),
('BSED', 'Mathematics', 10, 'Required for all programs'),
('BSED', 'Mathematics', 11, 'Required for all programs'),
('BSED', 'Mathematics', 12, 'Required for all programs'),
('BSED', 'Mathematics', 13, 'Required for Education programs'),
('BSED', 'Mathematics', 14, 'Required for Education programs'),
('BSED', 'Social Studies', 1, 'Required for all programs'),
('BSED', 'Social Studies', 2, 'Required for all programs'),
('BSED', 'Social Studies', 3, 'Required for all programs'),
('BSED', 'Social Studies', 4, 'Required for all programs'),
('BSED', 'Social Studies', 5, 'Required for all programs'),
('BSED', 'Social Studies', 6, 'Required for all programs'),
('BSED', 'Social Studies', 7, 'Minimum 600 hours'),
('BSED', 'Social Studies', 8, 'Required for all programs'),
('BSED', 'Social Studies', 9, 'Required for all programs'),
('BSED', 'Social Studies', 10, 'Required for all programs'),
('BSED', 'Social Studies', 11, 'Required for all programs'),
('BSED', 'Social Studies', 12, 'Required for all programs'),
('BSED', 'Social Studies', 13, 'Required for Education programs'),
('BSED', 'Social Studies', 14, 'Required for Education programs'),
('BSED', 'Values Education', 1, 'Required for all programs'),
('BSED', 'Values Education', 2, 'Required for all programs'),
('BSED', 'Values Education', 3, 'Required for all programs'),
('BSED', 'Values Education', 4, 'Required for all programs'),
('BSED', 'Values Education', 5, 'Required for all programs'),
('BSED', 'Values Education', 6, 'Required for all programs'),
('BSED', 'Values Education', 7, 'Minimum 600 hours'),
('BSED', 'Values Education', 8, 'Required for all programs'),
('BSED', 'Values Education', 9, 'Required for all programs'),
('BSED', 'Values Education', 10, 'Required for all programs'),
('BSED', 'Values Education', 11, 'Required for all programs'),
('BSED', 'Values Education', 12, 'Required for all programs'),
('BSED', 'Values Education', 13, 'Required for Education programs'),
('BSED', 'Values Education', 14, 'Required for Education programs'),
('BSHM', '', 1, 'Required for all programs'),
('BSHM', '', 2, 'Required for all programs'),
('BSHM', '', 3, 'Required for all programs'),
('BSHM', '', 4, 'Required for all programs'),
('BSHM', '', 5, 'Required for all programs'),
('BSHM', '', 6, 'Required for all programs'),
('BSHM', '', 7, 'Minimum 500 hours'),
('BSHM', '', 8, 'Required for all programs'),
('BSHM', '', 9, 'Required for all programs'),
('BSHM', '', 10, 'Required for all programs'),
('BSHM', '', 11, 'Required for all programs'),
('BSHM', '', 12, 'Required for all programs'),
('BSIT', '', 1, 'Required for all programs'),
('BSIT', '', 2, 'Required for all programs'),
('BSIT', '', 3, 'Required for all programs'),
('BSIT', '', 4, 'Required for all programs'),
('BSIT', '', 5, 'Required for all programs'),
('BSIT', '', 6, 'Required for all programs'),
('BSIT', '', 7, 'Minimum 486 hours'),
('BSIT', '', 8, 'Required for all programs'),
('BSIT', '', 9, 'Required for all programs'),
('BSIT', '', 10, 'Required for all programs'),
('BSIT', '', 11, 'Required for all programs'),
('BSIT', '', 12, 'Required for all programs'),
('BSOA', '', 1, 'Required for all programs'),
('BSOA', '', 2, 'Required for all programs'),
('BSOA', '', 3, 'Required for all programs'),
('BSOA', '', 4, 'Required for all programs'),
('BSOA', '', 5, 'Required for all programs'),
('BSOA', '', 6, 'Required for all programs'),
('BSOA', '', 7, 'Minimum 400 hours'),
('BSOA', '', 8, 'Required for all programs'),
('BSOA', '', 9, 'Required for all programs'),
('BSOA', '', 10, 'Required for all programs'),
('BSOA', '', 11, 'Required for all programs'),
('BSOA', '', 12, 'Required for all programs'),
('BSTM', '', 1, 'Required for all programs'),
('BSTM', '', 2, 'Required for all programs'),
('BSTM', '', 3, 'Required for all programs'),
('BSTM', '', 4, 'Required for all programs'),
('BSTM', '', 5, 'Required for all programs'),
('BSTM', '', 6, 'Required for all programs'),
('BSTM', '', 7, 'Minimum 500 hours'),
('BSTM', '', 8, 'Required for all programs'),
('BSTM', '', 9, 'Required for all programs'),
('BSTM', '', 10, 'Required for all programs'),
('BSTM', '', 11, 'Required for all programs'),
('BSTM', '', 12, 'Required for all programs'),
('Midwifery', '', 1, 'Required for all programs'),
('Midwifery', '', 2, 'Required for all programs'),
('Midwifery', '', 3, 'Required for all programs'),
('Midwifery', '', 4, 'Required for all programs'),
('Midwifery', '', 5, 'Required for all programs'),
('Midwifery', '', 6, 'Required for all programs'),
('Midwifery', '', 7, 'Minimum 800 hours'),
('Midwifery', '', 8, 'Required for all programs'),
('Midwifery', '', 9, 'Required for all programs'),
('Midwifery', '', 10, 'Required for all programs'),
('Midwifery', '', 11, 'Required for all programs'),
('Midwifery', '', 12, 'Required for all programs'),
('Midwifery', '', 15, 'Required for Midwifery'),
('Midwifery', '', 16, 'Required for Midwifery');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `applicant`
--
ALTER TABLE `applicant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `fullname_4` (`fullname`);
ALTER TABLE `applicant` ADD FULLTEXT KEY `fullname` (`fullname`);
ALTER TABLE `applicant` ADD FULLTEXT KEY `fullname_2` (`fullname`);
ALTER TABLE `applicant` ADD FULLTEXT KEY `fullname_3` (`fullname`);

--
-- Indexes for table `applicant_deficiencies`
--
ALTER TABLE `applicant_deficiencies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `batch`
--
ALTER TABLE `batch`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `deficiencies`
--
ALTER TABLE `deficiencies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`doc_id`);

--
-- Indexes for table `programs`
--
ALTER TABLE `programs`
  ADD PRIMARY KEY (`program_id`,`major`);

--
-- Indexes for table `program_documents`
--
ALTER TABLE `program_documents`
  ADD PRIMARY KEY (`program_id`,`major`,`doc_id`),
  ADD KEY `doc_id` (`doc_id`),
  ADD KEY `idx_program_docs` (`program_id`,`major`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `applicant`
--
ALTER TABLE `applicant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `applicant_deficiencies`
--
ALTER TABLE `applicant_deficiencies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `batch`
--
ALTER TABLE `batch`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `deficiencies`
--
ALTER TABLE `deficiencies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `program_documents`
--
ALTER TABLE `program_documents`
  ADD CONSTRAINT `program_documents_ibfk_1` FOREIGN KEY (`program_id`,`major`) REFERENCES `programs` (`program_id`, `major`),
  ADD CONSTRAINT `program_documents_ibfk_2` FOREIGN KEY (`doc_id`) REFERENCES `documents` (`doc_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
