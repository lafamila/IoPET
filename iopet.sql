-- phpMyAdmin SQL Dump
-- version 4.6.6
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- 생성 시간: 19-01-29 04:26
-- 서버 버전: 5.7.17
-- PHP 버전: 7.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 데이터베이스: `iopet`
--

-- --------------------------------------------------------

--
-- 테이블 구조 `chat`
--

CREATE TABLE `chat` (
  `CHAT_ID` int(11) NOT NULL,
  `ROOM_ID` int(11) NOT NULL,
  `CHAT_SEND` int(11) NOT NULL,
  `CHAT_TYPE` int(11) NOT NULL,
  `CHAT_MESSAGE` varchar(1000) NOT NULL,
  `CHAT_DATETIME` datetime NOT NULL,
  `CHAT_READ` int(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `chat`
--

INSERT INTO `chat` (`CHAT_ID`, `ROOM_ID`, `CHAT_SEND`, `CHAT_TYPE`, `CHAT_MESSAGE`, `CHAT_DATETIME`, `CHAT_READ`) VALUES
(1, 1, 1, 0, 'Hello!', '2018-10-18 00:00:00', 0),
(2, 1, 0, 0, 'Ok, Hello!', '2018-10-18 01:02:00', 0),
(3, 1, 0, 0, 'hello', '2018-10-18 19:09:26', 0),
(4, 2, 0, 0, 'bybye', '2018-10-18 19:10:20', 0),
(5, 3, 0, 0, 'bye\n', '2018-10-18 19:11:30', 0),
(6, 2, 0, 0, 'hi', '2018-10-18 20:02:09', 0),
(7, 2, 0, 0, 'hello', '2018-10-18 20:36:17', 0),
(8, 2, 1, 0, 'say yeah!', '2018-10-18 20:38:19', 0),
(9, 2, 1, 0, 'nonooooo', '2018-10-18 20:38:28', 0),
(10, 2, 0, 0, 'yeah!', '2018-10-18 20:38:49', 0),
(11, 2, 0, 0, 'eyah!!', '2018-10-18 20:39:04', 0),
(12, 2, 0, 0, 'say hoihoi!', '2018-10-18 20:40:12', 0),
(13, 2, 1, 0, 'hoihoi!', '2018-10-18 20:40:20', 0),
(14, 2, 1, 0, 'are you busy?', '2018-10-18 20:41:53', 0),
(15, 1, 0, 0, 'yeah...', '2018-10-18 20:42:09', 0),
(16, 2, 1, 0, 'busy?', '2018-10-18 20:44:38', 0),
(17, 2, 1, 0, 'oh...', '2018-10-18 20:48:09', 0),
(18, 2, 1, 0, 'no!!!', '2018-10-18 20:48:58', 0),
(19, 2, 1, 0, 'please answer me!!', '2018-10-18 20:51:24', 0),
(20, 2, 1, 0, 'hi?', '2018-10-18 20:54:00', 0),
(21, 2, 1, 0, 'please...', '2018-10-18 20:55:19', 0),
(22, 2, 1, 0, 'ummmm', '2018-10-18 20:56:35', 0),
(23, 2, 1, 0, 'ok.. then', '2018-10-18 20:57:17', 0),
(24, 2, 1, 0, 'I will find you', '2018-10-18 20:57:24', 0),
(25, 3, 1, 0, 'hello', '2018-10-18 21:32:51', 0),
(26, 1, 0, 0, 'asdf', '2018-10-18 22:27:07', 0),
(27, 1, 1, 0, 'fhgjhk', '2018-11-27 10:12:50', 0),
(28, 1, 1, 0, 'asasd', '2018-11-27 10:14:28', 0),
(29, 1, 1, 1, './static/picture/IMG_20181126_201449.jpg', '2018-11-27 11:03:42', 0),
(30, 1, 1, 1, './static/picture/IMG_20181126_201449.jpg', '2018-11-27 11:08:57', 0),
(31, 1, 1, 1, './static/picture/IMG_20181126_201449.jpg', '2018-11-27 11:12:22', 0),
(32, 1, 1, 1, './static/picture/IMG_20181126_201447.jpg', '2018-11-27 11:18:34', 0),
(33, 1, 1, 1, './static/picture/IMG_20181126_201447.jpg', '2018-11-27 11:21:55', 0),
(34, 1, 1, 1, './static/picture/IMG_20181126_201447.jpg', '2018-11-27 11:22:24', 0);

-- --------------------------------------------------------

--
-- 테이블 구조 `chat_room`
--

CREATE TABLE `chat_room` (
  `ROOM_ID` int(11) NOT NULL,
  `HOSPITAL_ID` int(11) NOT NULL,
  `PET_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `chat_room`
--

INSERT INTO `chat_room` (`ROOM_ID`, `HOSPITAL_ID`, `PET_ID`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 1, 5),
(6, 1, 6);

-- --------------------------------------------------------

--
-- 테이블 구조 `diagnosis`
--

CREATE TABLE `diagnosis` (
  `DIAGN_ID` int(11) NOT NULL,
  `DIAGN_NAME` varchar(30) NOT NULL,
  `DIAGN_DATE` datetime NOT NULL,
  `DIAGN_OPINION` varchar(1000) NOT NULL,
  `DIAGN_PRICE` int(11) NOT NULL,
  `HOSPITAL_ID` int(11) NOT NULL,
  `PET_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `diagnosis`
--

INSERT INTO `diagnosis` (`DIAGN_ID`, `DIAGN_NAME`, `DIAGN_DATE`, `DIAGN_OPINION`, `DIAGN_PRICE`, `HOSPITAL_ID`, `PET_ID`) VALUES
(1, '헤롱병', '2018-08-02 00:00:00', '헤롱헤롱 헤롱이가 헤롱헤롱해서 헤롱헤롱이', 0, 1, 1),
(2, '세균성 감염', '2018-08-03 00:00:00', '기운이 없고 털이 수척하여 내원\n피부에도 여러 발적, 탈모가 나타남', 0, 1, 1),
(3, '개 당뇨병', '2018-10-16 03:53:36', '\n나트륨이 과다한 음식은 잦은 소변과 심혈관계 질환을 유발할 수 있으니 피해주세요. 한 주에 30분 이상의 운동을 추천합니다. 정기적인 관리를 하지 않으면 쿠싱과 저혈당 쇼크등의 합병증이 유발될 수 있으니 유의해주세요.', 65800, 1, 1),
(4, '개 당뇨병', '2018-10-16 03:58:01', '진료해보니 진짜 당뇨병인거 같아요...!\n아닌가 ㅠㅠ\n맞는거같은데요?\n\n\n나트륨이 과다한 음식은 잦은 소변과 심혈관계 질환을 유발할 수 있으니 피해주세요. 한 주에 30분 이상의 운동을 추천합니다. 정기적인 관리를 하지 않으면 쿠싱과 저혈당 쇼크등의 합병증이 유발될 수 있으니 유의해주세요.', 65800, 1, 1);

-- --------------------------------------------------------

--
-- 테이블 구조 `disease`
--

CREATE TABLE `disease` (
  `DISEASE_ID` int(11) NOT NULL,
  `CATEGORY_ID` int(11) NOT NULL,
  `DISEASE_NAME` varchar(100) NOT NULL,
  `DISEASE_RECOMMEND` varchar(600) NOT NULL,
  `DISEASE_DIAG` varchar(600) NOT NULL,
  `DISEASE_RELATED` varchar(600) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `disease`
--

INSERT INTO `disease` (`DISEASE_ID`, `CATEGORY_ID`, `DISEASE_NAME`, `DISEASE_RECOMMEND`, `DISEASE_DIAG`, `DISEASE_RELATED`) VALUES
(1, 1, '요붕증 (  Diabetes insipidus )', '', '전체혈구검사 (CBC), 혈청 생화학적 검사, 세균배양을 포함한 요 검사, 복부초음파와 요 중 cortisol/ creatinine 비율 측정 또는 저용량 덱사메티딘 억제시험 , 변형 수분제한검사 (modified water deprivation test ) , Desmopressin 반응성 평가 , 무작위 혈장삼투압 ( Random plasma osmolality ) 측정 , CT, MRI, 신장생검, 정맥신우조영', '중추성 요붕증 : 특발성, 외상성, 종양 ( 두개인두종, 수막종, 혐색소성 샘종, 혐색소성 샘암종, 전이성) , 시상하부 및 뇌하수체 기형, 낭, 염증, 기생충, 뇌하수체 절제, 가족력 / 신장원성 요붕증 : 원발적 특발성, 원발적 가족력 ( Huskies 품종), 이차적 후천성 ( 41-1 참조 )'),
(2, 1, '내분비성 탈모', '', '염증 병력이나 임상적 증거 없이 대칭성 탈모증이 발생  *- 피부조직병리학적 변화 : 무핵각화층 각화과다증, 모낭 각화증, 모낭확장증, 모낭 위축증, 휴지기 모낭의 과다, 피지선 위축, 표피 위축, 표피 멜라닌증, 얇은 진피 , 진피 아교질 위축, 진피 탄성 섬유의 크기와 수량의감소 ( 저소마토트로핀증) , 과도한 모낭 각질화 (성장호르몬, 중성화반응 피부병) , 공포성 / 비대성 입모근 ( 갑상샘 기능저하증 ), 진피 점액성 물질 증가 ( 갑상샘기능 저하증), 두꺼운 진피 ( 감상샘기능 저하증), 여드름집 (부신겉질호르몬기능항진증), 피부석회증 ( 부신겉질호르몬기능항진증), 입모근의 결손 ( 부신겉질호르몬기능항진증) ', '갑상샘기능저하증, 부신겉질호르몬항진증, 수컷 개의 기능성 세르톨리세포종양, 암컷 개의 고에스트로겐증, 고프로게스테론증, 증가된 부신겉질스텔이드 호르몬 전구체, 뇌하수체 왜소증, Alopecia X, Feline endocrine alopecia, Telogen defluxion ( Effluvium ), 당뇨병'),
(3, 1, '고양이 말단비대증', '', '혈청 IGF-1 농도 측정, CT, MRI, 대부분 인슐린 저항성 당뇨를 보임 ', '뇌하수체 종양( Somatotropic cell의 기능성 샘종), 인슐린 저항성 당뇨'),
(4, 2, '개의 급성 후천성 망막변성 ( Sudden acquired retinal degeneration syndrome )', '', '신체검사, 혈청 생화학적 검사, 뇨검사 , 망막전위도 (ERG)', '부신겉질기능항진증, 시각신경염(감별필요) '),
(5, 1, '개 당뇨병(Diabetes mellitus)', '나트륨이 과다한 음식은 잦은 소변과 심혈관계 질환을 유발할 수 있으니 피해주세요. 한 주에 30분 이상의 운동을 추천합니다. 정기적인 관리를 하지 않으면 쿠싱과 저혈당 쇼크등의 합병증이 유발될 수 있으니 유의해주세요.', '공복혈당 수치가 100-125 mg/dL 또는 당화혈색소 수치가 5.7-6.4%인 경우 6~12개월 마다\r\n공복혈당 또는 당화혈색소 검사를 고려한다.', '췌장염, 백내장, 당뇨병성 케톤산증, 부신겉질기능항진증, 비만 만성 신부전, 갑상샘기능저하증/항진증, 종양, 글루카곤증, 크롬친화세포종, 글루코코르티코이드 약물, 프로게스테론-분비성 부신겉질암종');

-- --------------------------------------------------------

--
-- 테이블 구조 `disease_category`
--

CREATE TABLE `disease_category` (
  `CATEGORY_ID` int(11) NOT NULL,
  `CATEGORY_NAME` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `disease_category`
--

INSERT INTO `disease_category` (`CATEGORY_ID`, `CATEGORY_NAME`) VALUES
(1, '내분비계'),
(2, '안과질환');

-- --------------------------------------------------------

--
-- 테이블 구조 `disease_medicine`
--

CREATE TABLE `disease_medicine` (
  `DISEASE_MEDICINE_ID` int(11) NOT NULL,
  `DISEASE_ID` int(11) NOT NULL,
  `MEDI_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `disease_medicine`
--

INSERT INTO `disease_medicine` (`DISEASE_MEDICINE_ID`, `DISEASE_ID`, `MEDI_ID`) VALUES
(1, 1, 2),
(2, 1, 4),
(3, 2, 3),
(4, 3, 2),
(5, 3, 3),
(6, 4, 5),
(7, 5, 1);

-- --------------------------------------------------------

--
-- 테이블 구조 `disease_symptom`
--

CREATE TABLE `disease_symptom` (
  `DISEASE_SYMPTOM_ID` int(11) NOT NULL,
  `DISEASE_ID` int(11) NOT NULL,
  `SYMPTOME_NAME` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `disease_symptom`
--

INSERT INTO `disease_symptom` (`DISEASE_SYMPTOM_ID`, `DISEASE_ID`, `SYMPTOME_NAME`) VALUES
(1, 1, '다뇨증'),
(2, 1, '다음증'),
(3, 1, '배뇨실금'),
(4, 2, '대칭성 탈모증'),
(5, 3, '다뇨증'),
(6, 3, '다음증'),
(7, 3, '다식증'),
(8, 3, '체중증가'),
(9, 3, '신체크기의 증가'),
(10, 3, '복부와 머리의 비대'),
(11, 3, '하악돌출증'),
(12, 3, '흉곽외 상부기도의 폐쇄'),
(13, 3, '호흡곤란'),
(14, 4, '실명'),
(15, 4, '다뇨증'),
(16, 4, '다음증'),
(17, 4, '헐떡거림'),
(18, 4, '체중증가'),
(19, 4, '무기력'),
(20, 5, '다음증'),
(21, 5, '다뇨증'),
(22, 5, '다식증'),
(23, 5, '체중감소'),
(24, 5, '백내장');

-- --------------------------------------------------------

--
-- 테이블 구조 `hospital`
--

CREATE TABLE `hospital` (
  `HOSPITAL_ID` int(11) NOT NULL,
  `HOSPITAL_USER_ID` varchar(20) NOT NULL,
  `HOSPITAL_USER_PW` varchar(20) NOT NULL,
  `HOSPITAL_NAME` varchar(20) NOT NULL,
  `HOSPITAL_REVENUE` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `hospital`
--

INSERT INTO `hospital` (`HOSPITAL_ID`, `HOSPITAL_USER_ID`, `HOSPITAL_USER_PW`, `HOSPITAL_NAME`, `HOSPITAL_REVENUE`) VALUES
(1, 'lafamila', '1234', '아이오펫 동물병원2', 0);

-- --------------------------------------------------------

--
-- 테이블 구조 `medicine`
--

CREATE TABLE `medicine` (
  `MEDI_ID` int(11) NOT NULL,
  `MEDI_NAME` varchar(100) NOT NULL,
  `MEDI_INTRO` varchar(200) NOT NULL,
  `MEDI_SIDE` varchar(200) NOT NULL,
  `MEDI_WARN` varchar(200) NOT NULL,
  `MEDI_VOL` float NOT NULL,
  `MEDI_PERIOD` int(11) NOT NULL,
  `MEDI_METHOD` int(11) NOT NULL,
  `MEDI_DOSES` int(11) NOT NULL,
  `MEDI_PRICE` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `medicine`
--

INSERT INTO `medicine` (`MEDI_ID`, `MEDI_NAME`, `MEDI_INTRO`, `MEDI_SIDE`, `MEDI_WARN`, `MEDI_VOL`, `MEDI_PERIOD`, `MEDI_METHOD`, `MEDI_DOSES`, `MEDI_PRICE`) VALUES
(1, 'Mitotane (Lysodren)', '부신에 세포독성을 나타내는 경구투여용 약물이며 내부신종양, 부신피질기능항진증(쿠싱증후군)의 치료에 사용', '어지럼증, 구토, 무기력, 식욕저하, 멀미, 설사', '쇼크 및 심각한 외상이 있을 경우 즉시 투여중지할 것. 부신기능부전이 발생할 수 있으며 부신스테로드의 보충이 필요함. 간 질환이 있는 경우 투여용량을 줄일 것.', 500, 14, 0, 2, 32900),
(2, 'Prednisone (Meticortelone)', '일반적으로 피부, 관절, 폐 및 다른 기관의 염증을 치료하는 데 사용되며 천식, 알레르기, 관절염이나 혈액 질환 및 부신 질환과 같은 질병에 사용됩니다. 약사에게 문의하십시오.', '좌창, 홍조, 두통, 구역질', '헤르페스, 홍역, 결핵, 또는 수두, 신장 질환, 간 질환, 쿠싱 증후군, 당뇨병, 녹내장, 심장 질환에 비정상적인 알레르기 반응을 일으킬 수 있습니다.', 300, 3, 0, 3, 42000),
(3, 'Melatonin (Alopecia X)', '멜라토닌은 뇌 속의 송과선에서 만들어지는 천연 호르몬으로써, 시력이 좋지 않은 경우 멜라토닌 생성이 줄어듭니다.', '우울증, 호르몬 관련 병력', '멜라토닌을 복용하면 졸음을 야기시킬 수 있습니다. 장시간 운전할 때에는 복용에 주의하십시오.', 200, 5, 0, 2, 51200),
(4, 'Levothyroxine (씬지로이드정)', 'Levothyroxine Sodium: 대사, 성장, 발육 등과 관련된 일련의 단백합성, DNA transcription을 증가시킴. 산소 소모 증가, 호흡수 및 심박출량의 증가, 심박수 및 혈장량 증가, 지방, 단백질, 탄수화물의 대사증가, Gluconeogenesis 을 촉진하고 저장된 glucogen의 이용을 증가시켜 기초대사속도를 증가시킴.', '심계항진, 맥박증가, 부정맥, 협심증, 두통, 어지러움, 발한', '협심증, 진구성 심근경색, 동맥경화증, 관상동맥질환 등 심혈관계 질환 환자(기초대사항진으로 심부하가 증대되어 병세가 악화될 수 있으므로 투여할 필요가 있는 경우에는 투여개시량을 소량으로하고 보통보다 장기간에 걸쳐 증량하며 유지량은 최소필요량으로 한다)', 25, 3, 0, 3, 2190),
(5, 'Lutein (당근)', '색깔이 분명한 과일이나 채소 등에 고루 분포되어 있습니다. 브로콜리, 시금치, 케일, 옥수수, 오렌지, 키위, 포도, 오렌지 주스, 호박 등에 많습니다. 고지방식을 할 때 같이 곁들여 먹으면 흡수율을 높이기 때문에 단독으로 먹는 것보다는 식이와 함께 곁들이는 것이 좋습니다.', '귀찮음증', '루테인을 섭취하기 위해 야채를 꼭 챙겨먹읍시다.', 14, 365, 0, 3, 100);

-- --------------------------------------------------------

--
-- 테이블 구조 `pet`
--

CREATE TABLE `pet` (
  `PET_ID` int(11) NOT NULL,
  `PET_NAME` varchar(20) NOT NULL,
  `PET_AGE` int(11) NOT NULL,
  `PET_SPEC` varchar(20) NOT NULL,
  `PET_WEIGHT` float NOT NULL,
  `PET_SEX` int(11) NOT NULL,
  `PET_ADMS` tinyint(1) NOT NULL,
  `PET_PROFILE` varchar(600) NOT NULL,
  `PET_PERSON` varchar(10) NOT NULL,
  `PET_CONTACT` varchar(14) NOT NULL,
  `HOSPITAL_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `pet`
--

INSERT INTO `pet` (`PET_ID`, `PET_NAME`, `PET_AGE`, `PET_SPEC`, `PET_WEIGHT`, `PET_SEX`, `PET_ADMS`, `PET_PROFILE`, `PET_PERSON`, `PET_CONTACT`, `HOSPITAL_ID`) VALUES
(1, 'cola', 8, '포메라니안', 4, 3, 0, '털이 거칠고 피부에 발적', 'gb', '010-1234-6789', 1),
(2, 'cider', 2, '웰시코기', 3.4, 0, 0, '엄청 귀여움', 'km', '010-6412-3292', 1),
(3, '환타', 4, '사모예드', 6.1, 1, 0, '걸어다니는 귀요미', '압둘라', '010-1234-0985', 1),
(4, '스프라이트', 3, '시베리안 허스키', 5.8, 3, 0, '스프라이트 샤워하실래요?', '헨리', '010-4321-4321', 1),
(5, '토끼', 3, '사막여우', 5, 0, 0, '깡총깡총!', '햄찌', '010-2222-2222', 1),
(6, '햄찌', 1, '토끼', 2.6, 2, 0, '찍찍!', '사막여우', '010-1111-2222', 1);

-- --------------------------------------------------------

--
-- 테이블 구조 `stock`
--

CREATE TABLE `stock` (
  `STOCK_ID` int(11) NOT NULL,
  `STOCK_TYPE` int(11) NOT NULL,
  `STOCK_NAME` varchar(20) NOT NULL,
  `STOCK_PRICE` varchar(500) NOT NULL,
  `STOCK_TIME` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `stock`
--

INSERT INTO `stock` (`STOCK_ID`, `STOCK_TYPE`, `STOCK_NAME`, `STOCK_PRICE`, `STOCK_TIME`) VALUES
(6, 0, '기본진료비', '16500', '2018-12-02'),
(7, 1, '메모입니당', '수정할거지롱ㅁㅁㅁㅁㅁ', '2018-12-02'),
(8, 0, '혈액검사', '36500', '2018-12-02'),
(9, 0, '초음파검사', '50000', '2018-12-02');

-- --------------------------------------------------------

--
-- 테이블 구조 `user`
--

CREATE TABLE `user` (
  `USER_ID` varchar(40) NOT NULL,
  `USER_PW` varchar(40) NOT NULL,
  `PET_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `user`
--

INSERT INTO `user` (`USER_ID`, `USER_PW`, `PET_ID`) VALUES
('lafamila', '1234', 2),
('test', '12345', 1);

--
-- 덤프된 테이블의 인덱스
--

--
-- 테이블의 인덱스 `chat`
--
ALTER TABLE `chat`
  ADD PRIMARY KEY (`CHAT_ID`),
  ADD KEY `ROOM_ID` (`ROOM_ID`);

--
-- 테이블의 인덱스 `chat_room`
--
ALTER TABLE `chat_room`
  ADD PRIMARY KEY (`ROOM_ID`),
  ADD KEY `HOSPITAL_ID` (`HOSPITAL_ID`),
  ADD KEY `PET_ID` (`PET_ID`);

--
-- 테이블의 인덱스 `diagnosis`
--
ALTER TABLE `diagnosis`
  ADD PRIMARY KEY (`DIAGN_ID`),
  ADD KEY `HOSPITAL_ID` (`HOSPITAL_ID`),
  ADD KEY `PET_ID` (`PET_ID`);

--
-- 테이블의 인덱스 `disease`
--
ALTER TABLE `disease`
  ADD PRIMARY KEY (`DISEASE_ID`),
  ADD KEY `CATEGORY_ID` (`CATEGORY_ID`);

--
-- 테이블의 인덱스 `disease_category`
--
ALTER TABLE `disease_category`
  ADD PRIMARY KEY (`CATEGORY_ID`);

--
-- 테이블의 인덱스 `disease_medicine`
--
ALTER TABLE `disease_medicine`
  ADD PRIMARY KEY (`DISEASE_MEDICINE_ID`),
  ADD KEY `DISEASE_ID` (`DISEASE_ID`),
  ADD KEY `MEDI_ID` (`MEDI_ID`);

--
-- 테이블의 인덱스 `disease_symptom`
--
ALTER TABLE `disease_symptom`
  ADD PRIMARY KEY (`DISEASE_SYMPTOM_ID`),
  ADD KEY `DISEASE_ID` (`DISEASE_ID`);

--
-- 테이블의 인덱스 `hospital`
--
ALTER TABLE `hospital`
  ADD PRIMARY KEY (`HOSPITAL_ID`);

--
-- 테이블의 인덱스 `medicine`
--
ALTER TABLE `medicine`
  ADD PRIMARY KEY (`MEDI_ID`);

--
-- 테이블의 인덱스 `pet`
--
ALTER TABLE `pet`
  ADD PRIMARY KEY (`PET_ID`),
  ADD KEY `HOSPITAL_ID` (`HOSPITAL_ID`);

--
-- 테이블의 인덱스 `stock`
--
ALTER TABLE `stock`
  ADD PRIMARY KEY (`STOCK_ID`);

--
-- 테이블의 인덱스 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`USER_ID`),
  ADD KEY `pet` (`PET_ID`);

--
-- 덤프된 테이블의 AUTO_INCREMENT
--

--
-- 테이블의 AUTO_INCREMENT `chat`
--
ALTER TABLE `chat`
  MODIFY `CHAT_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;
--
-- 테이블의 AUTO_INCREMENT `chat_room`
--
ALTER TABLE `chat_room`
  MODIFY `ROOM_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- 테이블의 AUTO_INCREMENT `diagnosis`
--
ALTER TABLE `diagnosis`
  MODIFY `DIAGN_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- 테이블의 AUTO_INCREMENT `disease`
--
ALTER TABLE `disease`
  MODIFY `DISEASE_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- 테이블의 AUTO_INCREMENT `disease_category`
--
ALTER TABLE `disease_category`
  MODIFY `CATEGORY_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- 테이블의 AUTO_INCREMENT `disease_medicine`
--
ALTER TABLE `disease_medicine`
  MODIFY `DISEASE_MEDICINE_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- 테이블의 AUTO_INCREMENT `disease_symptom`
--
ALTER TABLE `disease_symptom`
  MODIFY `DISEASE_SYMPTOM_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
--
-- 테이블의 AUTO_INCREMENT `hospital`
--
ALTER TABLE `hospital`
  MODIFY `HOSPITAL_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- 테이블의 AUTO_INCREMENT `medicine`
--
ALTER TABLE `medicine`
  MODIFY `MEDI_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- 테이블의 AUTO_INCREMENT `pet`
--
ALTER TABLE `pet`
  MODIFY `PET_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- 테이블의 AUTO_INCREMENT `stock`
--
ALTER TABLE `stock`
  MODIFY `STOCK_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- 덤프된 테이블의 제약사항
--

--
-- 테이블의 제약사항 `chat`
--
ALTER TABLE `chat`
  ADD CONSTRAINT `chat_ibfk_1` FOREIGN KEY (`ROOM_ID`) REFERENCES `chat_room` (`ROOM_ID`);

--
-- 테이블의 제약사항 `chat_room`
--
ALTER TABLE `chat_room`
  ADD CONSTRAINT `chat_room_ibfk_1` FOREIGN KEY (`HOSPITAL_ID`) REFERENCES `hospital` (`HOSPITAL_ID`),
  ADD CONSTRAINT `chat_room_ibfk_2` FOREIGN KEY (`PET_ID`) REFERENCES `pet` (`PET_ID`);

--
-- 테이블의 제약사항 `diagnosis`
--
ALTER TABLE `diagnosis`
  ADD CONSTRAINT `diagnosis_ibfk_1` FOREIGN KEY (`HOSPITAL_ID`) REFERENCES `hospital` (`HOSPITAL_ID`),
  ADD CONSTRAINT `diagnosis_ibfk_2` FOREIGN KEY (`PET_ID`) REFERENCES `pet` (`PET_ID`);

--
-- 테이블의 제약사항 `disease`
--
ALTER TABLE `disease`
  ADD CONSTRAINT `disease_ibfk_1` FOREIGN KEY (`CATEGORY_ID`) REFERENCES `disease_category` (`CATEGORY_ID`);

--
-- 테이블의 제약사항 `disease_medicine`
--
ALTER TABLE `disease_medicine`
  ADD CONSTRAINT `disease_medicine_ibfk_1` FOREIGN KEY (`DISEASE_ID`) REFERENCES `disease` (`DISEASE_ID`),
  ADD CONSTRAINT `disease_medicine_ibfk_2` FOREIGN KEY (`MEDI_ID`) REFERENCES `medicine` (`MEDI_ID`);

--
-- 테이블의 제약사항 `disease_symptom`
--
ALTER TABLE `disease_symptom`
  ADD CONSTRAINT `disease_symptom_ibfk_1` FOREIGN KEY (`DISEASE_ID`) REFERENCES `disease` (`DISEASE_ID`);

--
-- 테이블의 제약사항 `pet`
--
ALTER TABLE `pet`
  ADD CONSTRAINT `pet_ibfk_1` FOREIGN KEY (`HOSPITAL_ID`) REFERENCES `hospital` (`HOSPITAL_ID`);

--
-- 테이블의 제약사항 `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `pet` FOREIGN KEY (`PET_ID`) REFERENCES `pet` (`PET_ID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
