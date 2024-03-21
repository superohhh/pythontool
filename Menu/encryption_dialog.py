#! /usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import os

from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QGroupBox, QLabel, QPushButton, QLineEdit, QFileDialog, \
    QTextEdit, QApplication, QVBoxLayout, QMessageBox, QDialog, QComboBox, QHBoxLayout, QRadioButton, QToolButton
from cryptography import hazmat
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

TUBIAO_copy_button = b'000001000400101000000000200093020000460000001818000000002000e4030000d9020000202000000000200067050000bd060000303000000000200023050000240c000089504e470d0a1a0a0000000d49484452000000100000001008060000001ff3ff610000025a49444154789c7d533d4b1c51143def63deec64867963d0cac6c64e5368699132ee0f30900d92ca6d1662957a0984c0a691145b0bf90f09c42ead60276211705d585c371f6ea2eccecede7937853ba2899b03a77a9c73cffd7802d3218410ec791e5656568224491c000c874351abd55ca552c98808629a5829c5a552e9e9783cae596ba33ccf19809052321171bfdfffd268345edf16a909bd8d8d0d9524c9e3858505dedbdba34ea73338393919b55aadb4d56aa5c7c7c7c34aa5c261187eb81d179ee7c1188352a90421c49b46a39133f388ef41bfdfff1d4511e922aee779cfd3347d0220027001e0d1ececec95732e2222d65a0300981942086459e64b29a195521c4551757171b1b9bdbd2db5d6b2dbed7e6b369bc32ccb72790d4829ef1814d044a4c3307cb1bbbb3b5e5a5a32001c8087ed76bb77797999ff674bd706e57259856118cccccc4822525996b131460e060375bbd25483492c97e739b4d670ce416b0d29259879aab0782b0cc4dfd59c7330c6301121cff39bbe8b194c66c27a5a852008b8dd6e1bad356bad0b779e1044943ae7a27f0c8ae8d56ab5b4b6b636989f9f7fb0babaea9859119107408c4623ecececc444f41eebebebfedcdcdcc1e9e9699ae73913912322c7ccbcbfbfffbd5c2e77e338be00f0d5f7fd8fc698cf003e0178c9cc12878787268ee3834ea733bcefe29879b4b5b5f54329f5360c43f8be0fdff76fee029ee7210882779b9b9b7c7676f6ebfcfc3cebf57aa3824747473f979797d3300c9fd5eb7509c0032071fd6f0400887abd1e0b2176adb5a9b596e238a6388e294992b1b5f6ca5afb4a298589f0cebafe0047164a4afb854ac30000000049454e44ae42608289504e470d0a1a0a0000000d4948445200000018000000180806000000e0773df8000003ab49444154789cb5554d4b2b57187ecec71827255e9c8ab8a8a0a2e522d68f402ad968c19d08726deba25a57b65da8b8742118c83fa871555c4ae1d69f2016a485825d14411ab9d06a8ddc38498c684c4c3267cedb8513afb5b926b7d0071e668633e7fd7cce7b80fac13cd60b5ed95437a494989d9d0dedefef7fe8388e26a2fbfd8c31524af1b6b6b6d2cccccccf4b4b4be70fd76b461e8bc5deb72ceb25805263632355a3699a24a5d4005e0783c1af0dc3a8cb389752c2b2ac978661502c16b353a9d4896ddba7a954ea9e95efc3c3c3c4c4c4840b400783c1896a066585bdbdbd0d00c4dcdcdcc700caebebeb69222a536d14060707affc7effef0f8df3ca8b10e29e00303434f4a9cfe7a3743afd97528a9452aeebbaba1a4ba5922622677575350b80e483c8753a9d0e0c0c0c7c6edb76a794d2a7b53619637f261289e7001cd7758510025a6bc639afda40ceefc4a3946a04a0a517b99e9a9a7aded1d1f17d3e9fff281008888a026e6e6e72994c86353434a87a55e18100700e808848eceeee7e675956573c1e3fbdb8b8b8cd6432b7994c2677747474b8b8b8f82b119117ddbb637272f21300859d9d9d936a1ddbdbdbb3015cd8b6fd9a88c8755dfdb6ee3a8e4344a4565656f2a8f4201e8fb79ba669864221e6ba2e79b5644a291242502e972b03a82dea2ae0b8ab91028072b9cc85108c31860a39e75c08f14e27be9a0306008cfd673b4f3bf83f519783071952bd86d95d39b4acf927009fcfa7186328168b426b0dc7712084a8ea4c29c5a494705d37cf18330100dddddd5f98a649e9743af148869a88e8eaeaea1c40767979f99a886e6bcc214d44767b7b7bbeb5b5f5b75a1930ad359a9a9a5aa2d1e8f1dadadab3cbcb4b39323252080402256f9d01001181734ec964b2717373f3d9d9d999130e87bffa4706a954ea7106a4b526ad351191138bc55e49296d0037004a00ca000a1ef3de332784f825140a85196377375a6767e78c6ddb5b8944e2acb9b9f9036f2c54d32c69ad6fb2d9ec794f4f8f5928142e171616beacf4c3711cded2d2928b46a37f388e03546ecc7038fc996118eaf4f4f49888a8582c92e338ffe2eded7df9f396651d1b86f1e31367e78d42373636da1863f6f4f4748688ae88c82122f5161693c9e489cfe7d39665fd40447c7474544622111e8944b867f8cd5d0d8033c6747f7fff37070707df0e0f0f67c7c6c6de735db7e1b1ee1963ecfafafa6a6b6bcb504a25c6c7c75f6c6f6f1f7b46f5936a9152a2afafef85dfef7f85bb59aebde743ba00a8ababeba7f9f9f94e4f3d4fce97bf01d38bbd1abe0fca660000000049454e44ae42608289504e470d0a1a0a0000000d4948445200000020000000200806000000737a7af40000052e49444154789ced574d68545714fece79f7be99219d7192492231da866051a13092686c2828224ab3304840a1e0465c24a0bbe02e1841ccce858b6ceba650dc05265db74684a494369a4a626d053166948c8999c9fcbd9f7bbac81b8d9ac44c2aaefac1c71bdee3cc77ceb9e7de730ff0dfc001abb2191c1cacd6665d7128a5a0b58688d07a544a4144486b0dcbb2deb2a72d8a13334b5757d797994ce64c2693395228146ca2f5ff4e4428168b65e3f178eae4c993a9818181f456f549298513274e9c8a46a36900b21912d1ebdf8d8d8dbf9f3f7fbe8399abf6800198e3c78f7f73fbf6ed94e338b567cf9e7d313030f0b2a1a1817ddf07f3fbcb6b8c81524a666666f8d2a54b3befdebd5b53575777ffd4a9535d9b56161102c022c24d4d4d3f0290fefefee7229295ea503c7af4681180b4b5b55d5e532ca8522ba00260b5b7b76b007cfdfaf5ddd168f4f9f6eddb173dcf7b668c11d7757ddff7cd461411e3baae2f22f2e4c9937f98b9d8d8d8286be9bf2953e6b708007d7d7d7b98b978e8d0a11722326b8c1111319b09dd1823c61829140a0ba150c803206a9530011066f68786863ebf71e3c6be582c566f8cd1c6183b9bcd86161717ef8f8d8d3507820c8037aafcb540441091b5ed9452686f6fbf188fc79f629d6aaea9a9f100789d9d9dcf4564ae12dc6633202292cfe75f85c3e1d719a0c1c141ba72e50aefdfbf7f607272f2b2effb4bdddddd7fc562b1cf88c8b8ae6b150a05934aa51ee6f3f930117d5d55d81f800500070e1c38180a8572d168f4ef8989892911c9bd1340b65028fc7ae7ce9d9f9879a1a3a323f3b13260b4d630c67c572e976b8686869c8e8e8eaf5cd7459076101189483412891c4c26932f01b8226fd5cf96c100c4711cca64326d0070eedc39df1803cbb28cd69ab4d6a49402338b31c6148bc53cb67e84afe90000c0f33c002011b1832df79e083333117d944ef69e03150467f627c3478de67f073eb503842dee0659e9ac5b73808864e558100f806f8ca9ca3ed8e225638c54e540a579d4d7d7a3a5a5c54c4f4fc71f3f7e1c6166944a25f8be2f9ee76d48c771849931313191731cc76f6d6df537ed003393effb00d0d4d3d3b398cfe7a5bfbfdf01301f0e87c9b22c524a6dc8502864f2f9fce3bebebe3aa554a8a5a5e56255c7697040a9ab57af36a452a9e99191917dc964d23b7cf87071f7eeddaf5cd72522826559febbb62282a9a9a9dad1d1d1baf9f9f9784343c3c8debd7b7fa87ca41d3b76fc0240161616664444825bcc7ba8bc4fa7d32fbbbbbb7f03f012808f95bee1055cf772aab52eeedab56bf8e6cd9b71225aa96211a1e6e6e69fe7e6e68e2c2c2c3cacadaddd638c11665eb3ca577d5b1a1f1f5f9e9d9d75c6c6c696878787bf504a855b5b5bbf4f2412cf5cd7b589c8ac5ac239cff3ee3d78f060bc5c2e03951a14116a6a6aba0d40161717a78d31eb66e0ddd61ac0999999f903c023adf57c7373f34ead35dee5aaa1e4f5166600b06d5be2f178168049a7d36522422080f558c944a954328ee3e8a5a5a528001d89448a914824e4ba2ebbaeab8227bbaecbbeef572eba08966465b633c660dbb66da300f8c2850bdb001495524c44d888cc4ce170986ddb463a9d3600b61391f4f4f4940198d3a74f0b00b38afeaa7a59416550bc76ed5a4322919804e09d3973e6cfa74f9fcee4f3f957cbcbcbd9b598cbe5b2b95c2e572a95666fddba359548241e69adfd643279918850d5002a22c4cce8edededa8afafbf17785b0887c3fe8768db761940d9b2ac6232991cd05abf29ae2a4100d0dbdbdbd2d6d636180c0d1fa46ddbd2d9d9e91e3b76ec5bdbb681954bcda67bc4bfc3ab2903712d4c600000000049454e44ae42608289504e470d0a1a0a0000000d49484452000000300000003008060000005702f987000004ea49444154789ced594f48236714ffcdce241d6cc428da832415aae2467b10b5ab54c1855095ea4d0939682f5e24c1838ab8070b2d0ac59b984b412994a2d48b08559488595a8dabac6b718b5b24a188bbe256bbb2d5dd3a8933f37ad88c4e8cae319928823f78e473f2f9bedfef7d2fdf9f370c11e126e3ce75138817375e0097e801464646ee4d4d4dd5fafdfe4f82c1a0feb2ffcfb2ac6c32995e58add659a7d3391dd18188126213131377b3b2b26601f8009006e6331a8d8f5d2e578d7a9c84901f1818f85243e211429a9b9b1f2863315aaf4293939377ebeaea7e0190a33cebececfcdde974fe9b9c9ccc310c73297f8140409a9898e05a5a5aca2549521efb7b7a7abeeeeeeefe59f3e887d28600504a4a0a89a2f88cb4c19b929292978a6fbd5ebfa6790a0d0f0fdf832a7534247f0c83c1709c4a1d1d1d2d9a0a686c6cfc5621dfd9d9b9a2357922a2e5e5e5e319b6582cdaa64f5959d94f8af38d8d8d878910208ae2ba3206cff314d346c630cc99a65ee793939313b2c7b02c9ba2b40541887e235b5d5d350882c003c0e2e222a6a7a79366666632bd5eef2b003b0082eafe975d6d62c57b058c8f8f7fdadfdfdf3637375721cbf21da896c6100e013c03f01680bcb5b59512e124d1382f9f1b1a1abec3c59b91044004200390398e7bab7cb7b7b7379788df0011bd54733873062a2a2a7ef47abd9fe324e2fe33baf100d2f02e7d8c003ee038ee3f51149334886bf4381df9f6f676074e22efb3dbedbf05028127674442080402fedddddd25005f0168cbcece7e882b9e8108013a9dee4f85fcc0c0c074140ea59005dbdada66af5a40580af5f6f6da8f8e8e3800309bcd87adadadd5514ce29d539f578ab041171616ca11cafbd1d1d1e7d741e8b20813b0b3b3f391d2b6582c86aba77379840920d5d19ae338f6cad9c4801b7f27be1570ddb81570ddb81570ddb815701ed49ba2c67e25f5df9a0a309bcd474adbeff707dfd737560882b0a5b4535353b515505b5b7b1c769bcdf69996be15f4f5f51d732e2c2c0cbfd01415158d2274ce3e3838988fe1acfe1aaa6ba8dbedf668780fa0fdfdfd059cdc057c838383f7b51640636363936a112e976b81de5d78e2c2e2e2e2ac8a3ce5e6e64ed1e9e26e7171f1e8caca8a0d000e0e0ebc0683a13c9669aeaeae7ee476bb33a0aa62141414bccacdcd7dcdb2ac2ccbf2712de9226c6f6f7fb8b4b494a92aec222929e9a9c7e3b1969696fea3f90c28686a6afa15da97d87de9e9e98f3c1ecfc70ae784092022dadcdc74e7e7e73fd140888fe7f93fd4ef05144be82b26b3d9fcc5dada1a88684b1084a5402010ccc9c911f7f6f6ee03a08c8c0c775757978be779f13c1f3a9d4e349bcd9b353535679576123b03674002f00380a3907d8fd05e743ab2d15ad83ec0b2acacb483c16022362209405288b404e0ef50c06246980093c9f44269cfcfcf1fc6e3f81cc8068341661846665956c8cfcf8ffbbc1126c06ab5ce2254466c6868c801f026de014e8fc7304c1911719224a5a4a5a56522ce1988c829a3d1f838e494eaebeb35adae0d0d0d4d01781ef2bf63b3d972cee311ad453c70b95c3550d5464d26d3d3f5f5f52949927c44b4735993657963777777b6aaaa6a41e5f72fbbddfe0d5419a0990022427373f30324f03d6f6565e5e0459910970022424f4f8f5dafd7af69298461189fc3e1688f2695e316a0584747478bc562219ee76322add3e9282f2f8f1c0e07adaeae9efbee205601ff031a456ef5773be7d50000000049454e44ae426082'
TUBIAO_key_button = b'0000010004001010000000002000440200004600000018180000000020002f0400008a02000020200000000020004c050000b90600003030000000002000df040000050c000089504e470d0a1a0a0000000d49484452000000100000001008060000001ff3ff610000020b49444154789c8d934d6b135114869f3913ce9dd4de6162acb126437adb846e8d5a44575d8820b8eb0fe8a66b9782742128fe99eedc0aba129b85fda01bb7da36202d0669aad0a473c7cd048b0acd0b87f7f0c27d38f7702fceb997aafa4d558f9d73eba55209e7dcbaaa1eabea9173eeb98800081014f547aafadd18e3acb56d55dd4ed3f4a6aa6e5b6bdb711cb754756f7171d11680b12ef61c020a44c026d02a3c020cf009a8028461c8eaea6ac45fa4a00098a2f7859ba2c266b3f9b356ab3d999e9ededcd8d8e8cecccc3c2ace87a5a2c98bbaa871360292c160f03a8ee3a7d6daab83c1e08588bcf5dee7c2e592d9d9d9a131e6a856ab7d3d383878e3bdd74ea7730df093004add6eb79f65596f7f7fff6118865e44fabd5eefee780797290088a2682fcff33bdefb00f83c1c0eef4d0ac801098260077022928bc847effd2d119908e08172bbdddef5de272b2b2b3a3737f7c17b7f636d6d6d0aa0075c0162a00bcc171e0316d8022a611852a954de351a8da520084892e47db3d9bc3fc90400a52ccbc8b2ecf0f4f47429cf73802f2727270fc6807fdff87f3255dd013a401086e196882c4b71c72170365e58e1671732008c317b405344f2288ade94cbe56531c64c1963ead6da54554d9aa6bf54d5586bd3388e1baaaaad56eb0c204dd3ddf3f3f3eb0b0b0bf3a3d1e876bfdfff8173eed584dfb92422341a8d674992f4abd5ea76bd5e7ffc1bdad8a23e734c028e0000000049454e44ae42608289504e470d0a1a0a0000000d4948445200000018000000180806000000e0773df8000003f649444154789ca5564f4c9c4514ffbd37b3331ffbedbaae09615784b488a506568a86501b4a09368d4d9b0609241cbc70f04022b16a3cf4c6c56b3d70f2d034a6ff12f0e0492b87466aaad59436e99f500d313dd070d8030b2e2efbfd7b1ef8105a4da8db974c3299f7e6fdde7b33f37e83e3c78fefcbe7f3f79859985972b9dcc2b163c7f6036011a18e8e8e33e9745a00483a9d968e8e8e335a6b00203c8be472b9796bed1d63cc69adf547d6dafb0d0d0db34a29747777bfe3384e25954a7d01e0742a953aeb384ee5e0c18347e3ed6a570066166bed874404228231e66322aac6bacf88e84fa536fd28a540446bcc7c26deae01d0c8c8888ae7fcb47f1d455154ad566d6c00cff30c800000a2288a004461183a0082300c35804844c2adf80004333333e10e9f0440b0c380e385201e8227eb4b00a258173da5f344a4aeb3b3f3bd6c36fbe9e0e0e0ab004444feb1d1bbd6f0bf8589082d2d2dfdaeeb7e2522f5beef0757af5efda45028bc4b44f7e2c0a37fd5ec198400845a6b148bc52f8320783c3c3c7ce0fcf9f3af28a512cbcbcbe33b6f592d00c06619100441c618f3cd850b177e1f1b1b5bb3d67eed79de406c1302a05a0004806666a452a9dbc964f28488701004a4b5beb3b1b1f1f2c4c4c44b71143567c0beefa3542add28954afb27272719800c0c0cfca4b536d7af5f3f0c00fdfdfdaa2600661611415757d782d6fac5478f1eb502c0952b571e0641505a585838c0cc989b9bab398308009a9b9b7f09c310737373dd00e0384e98c9646e2593c9a3f14187350144512400303d3dbd9c4824968bc5629b520a9ee7617d7dfd87d5d5d5c2c58b170d00a935030080b536725df786ebbafd8944022282dedede7963cc0b972f5f7e0ba8fd9a02003ccfc3eaeaeafccaca4a5b4f4f8f068042a1f0abe779e56bd7aebdf95c00449bdde0d0a1430bc61877efdebdaf03c0d4d4d47a26937968ad7ddb18533b80c8663f6b6a6afad9f7fd607676b61b00c23044a552992d97cbbdd56ab5a687b653d4a54b974ad6dae2dadada1b5a6b846188e6e6e6bb22d2303e3ebeef79013433c35afb635d5ddde12ddee8ebebbb2122343333d3fdbc00e4791e2a95cafccaca4acbe8e8a80300e7ce9d7b4c447f3436367ec0d8eef13a1e4f10463c676c33966ce95b5b5b05008e1c3972df5a9bae542a0500daf77d721ce7bb72b9dcc7ccccd6da2a1105441418633c22d200c0cc4c44ac94da001028a5368888995903c0e2e2a200407b7bfb2dcff3aa376fdeec544a05c964527cdf5f5f5a5a02f2f9fc1d6beded5d48ff2cb649ffaf2dd28fb998b4d6a8afafff3691483c705df774369bfdde1853ddb367cfe73875ea545b3e9f7fb0f3db72f2e4c9fff36d6111a1a1a1a1d772b9dcdd6c362b4d4d4dbf353636beaf94c2dfe41c8c6618a10e330000000049454e44ae42608289504e470d0a1a0a0000000d4948445200000020000000200806000000737a7af40000051349444154789cb5574d4c545714fecebdef6f9817665e20bca14867504c30089620bf459acc60a465819b5109c4346917f407b746178e5db8686143436a77eda2498d3bbbd0c45812120c69d2362d8d34c402a14231d5544d3450c6f74e17dc41c4a1467c9e6492c977bff3eef7ce39efdc7b303c3c6ca652a90f4b4b4b190003e0d2d2524ea55203994cc60240002893c958a9546ae0793cbca87574747ca069da3211dd06300360868896344dcb2693c9f7a594905222994cbea7695a968896f2f1344dc3b604b8aecb006e1f3d7ab4158001c0e8ebeb6b22a27b4545453f33333133151515fd4444f77b7a7a5ab6e08917de5c1903f8230f3e0f60118054bf45856dc5d3b7b3794eb588c7e3d606dc546bfe06cc57989987e7e579eee688e48dd03a383f3fbf7933e0e99cd2a6b5ad7802802fa5f4354d437d7dbdaeeac3479e1ad976deb63222f2d3e9f4ebfbf6edfba8acacecdae4e4e4cd442271a1baba7a17d6d2fd8c0806308bb5c2ca990ee01680053ca9810585e97978b7a05253535353535858380f8089e82111cd01e068343addd5d55586b54ffaa9170f42c0020043d334ecdcb9f33b005c5555f5e9f0f0f02e66d61289c40811f1eeddbb7b841050cf0b5c80c6cc545050709388fed4f527b453a74ebd2584f0f6eeddfb15333fd5b082ac01d2759d5dd79d05103973e6cc2e662622422412f9c5f7fd3b7373738d4494eba4810b1000108d462788a8706a6aaa81889899e9f4e9d30f5cd79d7bf4e851ecfcf9f36500a02211980006203ccfc3f4f4f40433e3ead5abb56a4d9752221e8f5f134238636363ed0070f6ec59dae8fcd25f41ae91b5b6b6be515050b06a18c637966501804e44701ce71000b66dfb33e5ab051901e8bace0070fdfaf559d33417c2e170dbf2f27211802c33a3b5b575311c0e6799798f3a373ca8620caa0fe800c8300c4829bf0d8542defefdfbeb144f3073281289fc1a8944ee8f8c8cc401209d4ecba0050800705df7132262c7713a8908004c2104a4945f4829d9719c36e52f036dc544e403405757d7a46a3c6fe6ce01dff7d1d0d0f03b33a3bcbcbc4ee1db3fc3ffcfeaeaea267cdfbfb7b4b4d4bebaba4a001e03407777f738807f5756560e65b3590a5c00f35a7f19181858b22ceb9fc5c5c50a2292508d676565e50680bf676666aa8f1c39220217a08c9819151515bf31b33338385895c3cf9d3bb79a48246ef8be5fdcd8d8b8077805c73100a1eb3a5b96354a44f6e8e8688bc23500701ce70a11d9972e5d3a907308f22b58dfc8b2ac7621049ba639a4700b006cdb3e208460c3303e1742041f81743acd00d0dbdb7b271c0eaf0a216a6ddb06802c009c3c79f22fdbb61f8642a17acff34240c011c85d369839148d467f741ce7cef8f8f86b8a2f9859dab63d1a0e87970f1f3ebc277001caa4941244f4a56118beebba4d0a370120140a0d121197979777bf923e00803ccf436565e57c369b25c330e2ea26c400d0d9d939c5cc686b6bbbb02e201e8f6f1493fbcf1b30deb4b6150f994c26d7117f22222e292969f73c8f0078994c46d4d6d68e01b83b313161e59c831e4c08008686868a01dc2d2e2efe419d096b6a993522ba699a26e746b3a5dedede66a891ebf8f1e38d5b8c66f7fafafa9ab6e03d93cedc750cc08363c78e355dbc78d1e8efef7f7bc78e1d5f03785c55557505c964f263359ce61d3a5f6238254dd370f0e0c177755d5f557eb3007c9596ef9b9b9b2ba1c6f381582cb63e76c762314ea55227f28ce7279ec7db9406ba7cf9b2d9d1d1d11f8bc5b8a4a4845b5a5a6ec4e3f177547af01fdf9518275a1e1c5e0000000049454e44ae42608289504e470d0a1a0a0000000d49484452000000300000003008060000005702f987000004a649444154789ced5a4f48235718ff119da06199c846413d18ad5a1b34e24cd28213d43214fc735845173c78f0e2494c90f65ee8a184a47ad01eea52a447d152a5201e348b48716cddcc6a74d1ec462a7a28a5d4821e6c3195d7c3fad2719c3131c6ce1cfae0c137f3fdbe6fde2ff37ef3be993c10424008412814eae1799e300c43001000846118c2f33c0987c3bd14a7d543a1506fb6b1f7ed20844014c5af00bca617d7e80951149f69251045f119804436b13921100e879f28069fd0e9044022180c3e550687c3e15ea5ff2eb13923c0f37cea971a1e1efe580df0fbfd013a108ee3be55fa789e9fcd3636670414f336a10bba1a04c330fbcaf30cc3ec671b9bab6e492693c8b42593c9fcdb8eef129bab667988a4ff65fb9f80d1cd1404229148e5c8c8c8685353d377369b6db7bcbcfc87c1c1c14f338dcff829a4c6e89dcf14b3b9b9f9b8bebefe7b682f84899292928d783c9e7feb63d42802f1783c9f6559593d685c5f00494b4bcb37a624303030f019bd766161e1aedfef0facacac541242b0b0b0d090979797aa0e7676766ca623e0743a9fd3f34b4b4befaae37a7a7abea0639b9c9cecd25dc832154aaedbd9d9194bedcecece376abfcfe75ba7b62449cd7a790c23505b5b9b1af4f2f2f23b6abf200812800300d8d8d810f4f21846c0e3f1c857664d341af5aafd8220fc565050f017001c1d1d55e8e5318c80d7eb8d525b96654f3acccccccc075a18a3091c00802ccb37ee00000882b07165d64892a4398d0c23d0d8d8786eb3d9ce01fd29a2d4819e900d2d25388edba6f6e2e2e27b6a7f7777f72b6ac762b126ad1c8612f07abd2faecc1abd69545757f706002e2f2f2d9148a452ed379480c7e37949ed6834aa29644110e87aa0a903a3ef405a21fb7c3e89da9224f9b4308655a38410d8ed76f936ffdede9e95e6b0dbedb2694a09da789e4f4da3f9f9f946b5dfe5725d141717ff0e00a7a7a7ecf6f6f623a5df7002ca15596f1a353737ff4831eab2c270022a1da413b2a60e0cd58012e370387ed2f2afadad95534c5555d58aa93400000e87e30f0038393979ace56f6d6dfdc56ab55e00c0e1e161a5d2670a02caa26d76765653074ab1cfcdcdf1d436058174a535a05fd8998540264256bee05c2bec0c17b112c7b2ec8dc54a8d517e2836c51d0080b2b2b25f81b7efcafbfbfb562d4c7575f5cfc0db0fc5ababab158049a610909a46c02d3a50bce8a774601a025eaf970a19b7085959d835032622908590534f2253885889b5d96c313d4c5151d10b9a6f7777b7c0347700002a2a2a8e01e0fcfcdc168bc51e696194859d24497f9a8a806245ae916599d7c2280bbbf5f575f36800b8b622a71332d581e908bcc4d5e0a2d1e8fb5a1851148fa97d7c7c0c0bc330195f806198bf6f3bbe4bac566b6f6f3fa0762c16bbf1760600d3d3d31f52bbb4b41416b7db9d72060281803a6074747484da0d0d0daf943eb7dbbd936dac5ea3b88b8b0b2bcdb9b5b5c58e8d8df5b4b5b54d0f0d0d7d0da006c0415757d727f7da2ef0105b0dc6c7c79fe8e4bcf64f8ed3e97c4ec8bf9b3db2deb0f1109b3d3a3a3abed4c999b0582caffbfbfb3f4fad1dd40806834f398ebbb16586e33892eed7bb4fac5e9f9898e8e2799eb02c4b5c2e17e9ebeb235353531fa971ff00818897db60862b820000000049454e44ae426082'
TUBIAO_clear_input_button = b'000001000400101000000000200033020000460000001818000000002000790300007902000020200000000020009a040000f20500003030000000002000240400008c0a000089504e470d0a1a0a0000000d49484452000000100000001008060000001ff3ff61000001fa49444154789c9d923f8c126110c567f61f0442b2a190e2d850c0164bcc52d11039a3065b484868cc41a105a131161624b6f634d79098987825d8509918132ba97731d010932bb43047852c7bbbdeb3708145a4d029bfccfbcd9b371fd3bf9744447e2693b92708c2abff11533e9fbfa3aaea674dd31e1e6b1482668988c4b0d8308cb2aaaa5f745d2f33f35fc5221191288a2449120982b0016e26cf73b9dcdd30744f1c084e88e88c889e12d1035996c9308c535555e7baae9f86c51b0f0211b1a2283f0541686a9af6b25eafdf4aa552188fc7de7038fc148d46d5743afd7c369b7d0cc4fe762a3353241221227a522a95968ee35c03b806e00170fafd3e1445792749d276c55d5abf2ddf66e661ad565b562a95cbe9747a05008ee3dc789e07004ea3d1588aa2783fe8df411289c479b158fc3a180c7c002bcbb216a669ce6ddb5e6c2000bc5eafe711d1b3c0c52e3c66fed06ab50060e9ba2e006032992c0a85c21602c0eb76bb1e11350fd690659988e875bbdd06805518629ae67c3a9d5ef9beef66b3d96fc964f224b8bdb017030026a28b4ea7b307b12c6b51a9542ecbe5f28f582cd60cff89707108f26603711c0700dc6ab5ba22a2c78aa21c5ee008e4225867391a8d7c5996df06273ef875e147048132803366f65dd77d64dbf677667eb15eaf99996f8e4d3f7012d87d1f8fc7cf0feefe47fd024029f87156110e250000000049454e44ae42608289504e470d0a1a0a0000000d4948445200000018000000180806000000e0773df80000034049444154789cad944148235718c7ffefcdbc19d68d058dc1938d0a6a32266c62a2e021878087165ae9a1161672f0268258575a963d050febb13d285ed44b40ebadbd7bf4162882d04bac60da5d57536da831bbc964defb7ad891466ab209eb07c3c03bfc7e8ffff7f8030f3b0c001742607070f079381ca687866b42088c8e8e2e0921a4dfef7ff1e070cbb29685106459d6b261180f0e7f2684a06030f8bdaeeb00a0b50c49a7d33c9d4e7317d80cfe5d1d9cdd07ab1fee7eff3b7765fc63e1304d13abababded9d9d9f1542af52493c93c164200003e06ae31c630363616334df3270079d334af0dc3b806f07b4747c78fe974fad36030f8ad61186dc119005dd7758442a114806232997cb7b7b7f7f7c9c9c99fc7c7c7af3637372f2dcbba01f04ad7f5d2f0f0f072ab700defe90887c39f777676963636365e13d13f74772411bd999e9e2e0238dfdedef6e1bf9d34cc9a33c6b0bfbfeff5f97c2f01947b7a7a8a4474464454a9549494524929956ddbb7a273cbb26e3c1ecf0fee4e1a0a6018068686869e02f86d6060e07a7777f7746a6a2a1f89444e89e88288484aa96ec9b66d2b22a2adadad2bc6d8712693795c17f1dd49241263dddddd3f1b86515d5858b8ac542ae744241dc7298c8f8fe763b1d8a994b2502f711c4729a52897cbbd16425ca752a92700705f4c3c97cbfd5a2c16bfca66b36fd6d6d63e314db3d7711cae699a2f9bcd3ee29cb3898989b74aa9bf38e74c29458c3130c6c03927f76f36ccdfebf57ec3397f97c9643a0138524a689a06a51401f065b3d9478cb13b12c77108000e0f0f3b6cdb2e0602811300585959b9bf3d474646be04509b9b9bbb20a2b2528a9452f5b917e2f1f86d5c17ee59299148544dd3dc734bade19205630cd168741a406d7e7ebea124168be52391c869b55a3d5b5f5f3f03508ac7e35197d3b4d8f456248ee31492c964beafafefcae3f19442a1508a73def4f62d498848dd3ecd9d9d9d3f0094a3d1e8679aa67df0e62d49a49424a5a45aad56e8efef2ffb7cbe976e3de8edc09b49de1291bdb8b8780920777070d005406b560f6d49969696ae8e8e8ef2866154fd7eff53c618666666da8aa6a12410087c01e00680eaeaeafae5434fb2dd118c315896f5756f6f6f797272320adc5f098de65f4b96ee45f9c7762a0000000049454e44ae42608289504e470d0a1a0a0000000d4948445200000020000000200806000000737a7af40000046149444154789cbd574b481c771cfee6b9ce607737d1d58362705fb7eca52878901022ba84402bd4061b7a7083074f22a26ec821c7d2bb07030939086d301444c8295008121b890a75d7c454e3a269c5a8f191dd24d5999daf0767edb67175e3eb83616698f9ffbec7ff31ff014e11b76edd1201607d7ddd5d5151f14b7d7d3d4f9d7c7e7efe8cdfefff09002b2a2a064f957c6d6dcde5f57aef03a0dfef1f585858387b6ae4f178fc6c2010b80f805eaff7412291709f1a79b6739fcff7607474b428fbf98992e772ded4d4241dba38492173ec477eecceed86ff572e67bb3929e7bb8a2549024995a48ba42c49ffa92701c7ef5c040092527373f3d705050577745d7fa269da8b82828267aaaade0b87c3d7484aa2281ebf735996110e87abdc6ef76f00280882555959b91e0a853682c1e0a6aaaa06802d97cbf5341c0e5f2e2f2fef3f16e7172e5c906df26f64597e278aa2d9d9d9f92a168b2d935cc81cb3b3b37ff5f4f4cce8babe01c00260959595fd3c3c3c7ce6b0ce25d8b137363656298ab21908041662b1d81cc92dee8d8fb1586cdae3f1ac4b92c4bababacb59b5f2869069e0703870f1e2c5ef45517c23cbf2878989891992340c83a669329d4e5b24ad743a6d99a66999a64992d6d4d4d4b4d3e9dc70b95c4f49e64dbe4b2c8a22dadadabe2c2d2d7d0860dbe1702401a4babbbb5f907c4b3243fe096c115b376fde9c01b0555f5fff1d905f17888220e0d1a347453e9fef070049555553914864767171712e1a8d3e0790eceeeefe9de46a2e11a6695a9665716666665155554355d57bf614dd5f80a228a8adadbd5658581807903e7ffefccac8c8c84b921fecdaab376edc9804f0beabab6b32571259f77f0683c14d87c3f18ca40cecac9c390578bdde5145514ca7d369f6f5f54d915c2649cbb2681846a6e85a341a9d04f07e9f2432d7af43a1d086a669d3249d070a0804020900acaeae5ec914dededede2d9c45b29a11b1571259efbd3e77eedc86aeeb4f48aa070ae8eded2d2c2e2efe1500af5fbf9e2099cc24b087889c4964cd84378aa2989aa6dd9165f9e03100008383835f783c9e11008c44227324539665319d4eef2562cf240cc32049a3b3b3f31580edab57af7e05e4370b2400181818709594943c06c0d6d6d63992a9fd92e8e9e9c94e628524e3f1f82b5555d36eb77b7700e60b3193446969e9937c93b04524a3d1e8f4d8d8d81f7ebf7f4192a4cd4b972e5565d7cd171200dcbe7dfb739278dbd5d5f51c404a519494a2289b0d0d0ddf2a8a72b44f6f3e4998a66991e4d2d25242d3b4a42008cb57ae5ca9b1179f23edf5f24ac23e7f8c4422b300b6eaeaea9aedf69fd5f7b9903309f2df75627c7cfca5aeeb298fc7f3d09eebc7bacbcd9544d2ee85955028b42249d2dfadadad5582201c6da79b039f24d1d2d29220b97af7eedde7000c9fcff7a3288abb824f02bb491415153d06c09a9a9a15a7d3b9a5ebfaf4d0d050b1fd5eeee5f6182002407f7fbfd3e3f13cc6cede305d5b5b7b0d38e24fc667400280f6f6767730187c59595939d6d1d1a16167d41fdafd3f3e05236a5eb8359b0000000049454e44ae42608289504e470d0a1a0a0000000d49484452000000300000003008060000005702f987000003eb49444154789cd5d84d481b5900c0f14747ca3294454cf023a71e34f0c01172504a5cab27853d043d0d2818285d67298b1a902ab227d99caa1172521b4d82de7b4b0e0a494845da4accc71a09932161613797526ae816a24c5e2f7d769a9a34f3e625990e3c0881ccfbff5e5e32c9008410f8d1c6eaeaea2393c984d6d7d75b1fa376cccdcd3d0500880000d4d3d3d3fa20d2780080b8b4b4f47bcba348e3ed76fb9f0821d0f2302df13f04a056bcee01df8bd735a09e78dd02ea8dd725404dbcee006ae375052089d70d80341e2104da00c523100898b3d96cefe5e5653bcbb21f8d46e35b8bc5121b1818f858ed3582203cddd9d9f90d00d00b00c8daed76bfcfe7fbabee49b5ae5e3018ec9d9c9c7cc6304c067c5945e5103b3b3b8f171717ffa0b9f29ab7502a95fa89e3b81755a26f1b22c33099e5e5e5c7b4e28901bbbbbb0f59964d2803218479a7d379120e874392244524498a84c3e110cff34908615e0931180caf68c413015c2e974db9ea56ab552c140a5184908caa1cb22ce73737378f2b209ae355038e8e8eee7fdeeb084298dfdede7e8910baae165e79148bc5d71cc7e530a0bdbdfd8d96785580783c7ecf68349e54c4ab3e6459ce2a10e2cacacae386031c0ec793b6b6b60bbc72e3e3e31724f1f828168baff176621826d330c0fefefe0393c914a9fca68110e6e3f178480bc2ed761fe377c1e1703ca10a482412ece8e8e8ae321c429817042186574e2b4296e57ff0b9bababa8ea9012ab70b84303f3d3d9d28954a4984104aa7d3615a089ee793f85d482693ac26c0c1c1c137db85e3b89c244991ca89692142a15008cfe5f3f97e21026432993b636363cf2bb78bc7e38922843e549b9c06229bcd86f19c1b1b1b362280d96cfeea92cff37cb2542a25ea09d08a90242982e75d5b5b9b26020c0e0e7e052897cbffaa89383f3f274628b790dbedfe9508707a7a6ae8e8e878874f64b3d9fe4608bd6f06c2e9749ee00f7120103013011042ad425cd3b898dd3c6836a2502844f15c535353cf34039a8cb8b65aad373fa783c1602f15002d442a95aa89d8dada7a89cfdfdfdfff8234fe5640a3111e8f278a9f675936417a05ae096814626262e242f1a746dcdbdb7ba825be26a011083c1886c9b85c2ea22baf2a002d84200831fc7a83c1f0eaf0f0f03e8df8ba005a1157575729e5f77d2c16fb99567cdd002d889999197cf7425c5858f8e6de50d30024885c2e17c1abdfdddd1da51daf1aa012f1bfc56291f0eafbfd7eab2e00f522bc5eefcd4f859191116f23e28901df43547e70cfceceeee90e500d512e97ff9b9d9d8de3ad333f3f3fdfa878cd80db10caa1e56e43d3003510a2d7eb25faa3de74c06d88e1e1617fa3e3a9023062686808f5f5f5a1743a7db719804f6ab211f1b803c5ae0000000049454e44ae426082'

class EncryptionDialogHandler:
    def __init__(self, parent=None):
        self.parent = parent

    def open_encryption_dialog(self):
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("加密解密文件")

        self.aes_key_label = None
        self.current_operation = "encrypt"  # 初始选择加密操作

        # 创建布局
        layout = QVBoxLayout(dialog)

        # 添加加密方式标签和下拉框
        encryption_label = QLabel("加密方式:")
        layout.addWidget(encryption_label)

        self.encryption_combo_box = QComboBox()
        self.encryption_combo_box.currentIndexChanged.connect(self.toggle_encryption_components)
        encryption_methods = ["AES--对称加密", "RSA--非对称加密", "SHA-XXX--哈希函数"]
        self.encryption_combo_box.addItems(encryption_methods)
        layout.addWidget(self.encryption_combo_box)

        # 类别分组框
        category_group_box = QGroupBox("类别")
        category_group_layout = QVBoxLayout()
        category_group_box.setLayout(category_group_layout)
        layout.addWidget(category_group_box)

        # 添加哈希函数标签和单选框
        self.hash_function_label = QLabel("哈希函数:")
        category_group_layout.addWidget(self.hash_function_label)

        # 创建水平布局用于放置单选框
        hash_function_layout = QHBoxLayout()
        category_group_layout.addLayout(hash_function_layout)

        # 添加单选框
        self.sha256_radio = QRadioButton("SHA-256")
        self.sha256_radio.setChecked(True)
        self.sha384_radio = QRadioButton("SHA-384")
        self.sha512_radio = QRadioButton("SHA-512")

        # 将单选框添加到水平布局
        hash_function_layout.addWidget(self.sha256_radio)
        hash_function_layout.addWidget(self.sha384_radio)
        hash_function_layout.addWidget(self.sha512_radio)

        # 添加哈希函数单选框和标签到布局中
        category_group_layout.addLayout(hash_function_layout)

        # 添加 AES 密钥选项（默认隐藏）
        self.aes_key_label = QLabel("密钥长度:")
        self.aes_key_16 = QRadioButton("16字节")
        self.aes_key_16.setChecked(True)
        self.aes_key_16.toggled.connect(lambda: self.limit_aes_key_edit_length(16))
        self.aes_key_24 = QRadioButton("24字节")
        self.aes_key_24.toggled.connect(lambda: self.limit_aes_key_edit_length(24))
        self.aes_key_32 = QRadioButton("32字节")
        self.aes_key_32.toggled.connect(lambda: self.limit_aes_key_edit_length(32))

        aes_key_layout = QHBoxLayout()
        aes_key_layout.addWidget(self.aes_key_label)
        aes_key_layout.addWidget(self.aes_key_16)
        aes_key_layout.addWidget(self.aes_key_24)
        aes_key_layout.addWidget(self.aes_key_32)

        # 添加加密模式标签和下拉框
        self.encryption_mode_label = QLabel("加密模式:")
        self.encryption_mode_combo_box = QComboBox()
        encryption_modes = ["ECB电子密码本模式", "CBC密码分组链接模式", "CFB密码反馈模式", "OFB输出反馈模式",
                            "CTR计数器模式"]
        self.encryption_mode_combo_box.addItems(encryption_modes)

        aes_key_layout.addWidget(self.encryption_mode_label)
        aes_key_layout.addWidget(self.encryption_mode_combo_box)

        category_group_layout.addLayout(aes_key_layout)

        # 添加 AES 密钥编辑框和随机按钮
        self.aes_key_edit = QLineEdit()
        self.aes_key_edit.setPlaceholderText("输入KEY（点击右边按钮可随机生成）")
        pixmap_key = QPixmap()
        pixmap_key.loadFromData(QByteArray.fromHex(TUBIAO_key_button))
        self.random_key_button = QPushButton()
        self.random_key_button.setIcon(QIcon(pixmap_key))
        self.random_key_button.clicked.connect(self.generate_random_key)

        key_layout = QHBoxLayout()
        self.key_label = QLabel("Key:")
        key_layout.addWidget(self.key_label)
        key_layout.addWidget(self.aes_key_edit)
        key_layout.addWidget(self.random_key_button)

        category_group_layout.addLayout(key_layout)

        # 添加 IV 输出编辑框
        self.iv_label = QLabel("Iv:")
        self.iv_edit = QLineEdit()
        self.iv_edit.setPlaceholderText("IV初始化向量（默认随机生成）")

        iv_layout = QHBoxLayout()
        iv_layout.addWidget(self.iv_label)
        iv_layout.addWidget(self.iv_edit)

        category_group_layout.addLayout(iv_layout)  # 添加到布局中

        # 添加工作区域分组框
        Job_group_box = QGroupBox("工作区域")
        Job_group_layout = QVBoxLayout()
        Job_group_box.setLayout(Job_group_layout)
        layout.addWidget(Job_group_box)

        # 创建单选框用于选择加密或解密
        self.encryption_radio = QRadioButton("加密")
        self.encryption_radio.setChecked(True)
        self.decryption_radio = QRadioButton("解密")

        # 设置单选框水平布局
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.encryption_radio)
        radio_layout.addWidget(self.decryption_radio)
        Job_group_layout.addLayout(radio_layout)

        # 添加"密钥大小："标签和单选框
        self.key_size_label = QLabel("密钥大小:")
        self.key_size_2048 = QRadioButton("2048")
        self.key_size_2048.setChecked(True)
        self.key_size_3072 = QRadioButton("3072")
        self.key_size_4096 = QRadioButton("4096")
        self.key_size_custom = QLineEdit()
        self.key_size_custom.setPlaceholderText("自定义大小")
        self.key_size_custom.setMaximumWidth(100)

        # 添加单选框到水平布局
        key_size_layout = QHBoxLayout()
        key_size_layout.addWidget(self.key_size_label)
        key_size_layout.addWidget(self.key_size_2048)
        key_size_layout.addWidget(self.key_size_3072)
        key_size_layout.addWidget(self.key_size_4096)
        key_size_layout.addWidget(self.key_size_custom)

        # 设置单选框到类别分组框
        category_group_layout.addLayout(key_size_layout)

        # 添加"生成密钥对"按钮
        self.generate_key_pair_button = QPushButton("生成密钥对")
        self.generate_key_pair_button.clicked.connect(self.generate_key_pair)

        # 在 key_size_layout 布局中添加生成密钥对按钮
        key_size_layout.addWidget(self.key_size_custom)
        key_size_layout.addWidget(self.generate_key_pair_button)

        # 添加公钥和密钥标签及编辑框
        self.public_key_label = QLabel("公钥:")
        self.private_key_label = QLabel("私钥:")
        self.public_key_edit = QLineEdit()
        self.public_key_edit.setPlaceholderText("公钥用于加密")
        self.private_key_edit = QLineEdit()
        self.private_key_edit.setPlaceholderText("私钥用于解密")

        # 创建水平布局
        public_key_layout = QHBoxLayout()
        private_key_layout = QHBoxLayout()

        # 将标签和编辑框添加到水平布局中
        public_key_layout.addWidget(self.public_key_label)
        public_key_layout.addWidget(self.public_key_edit)
        private_key_layout.addWidget(self.private_key_label)
        private_key_layout.addWidget(self.private_key_edit)

        # 将水平布局添加到类别分组框的布局中
        category_group_layout.addLayout(public_key_layout)
        category_group_layout.addLayout(private_key_layout)

        # 添加输入和输出文本框以及按钮
        self.input_text_edit = QTextEdit()
        self.input_text_edit.setPlaceholderText("请输入内容")
        self.input_text_edit.setStyleSheet("border: 1px solid gray;")

        # 创建工具按钮并连接复制功能
        pixmap_copy_button = QPixmap()
        pixmap_copy_button.loadFromData(QByteArray.fromHex(TUBIAO_copy_button))
        copy_input_button = QToolButton(self.input_text_edit)
        copy_input_button.setIcon(QIcon(pixmap_copy_button))
        copy_input_button.setToolTip("复制内容")
        copy_input_button.clicked.connect(lambda: QApplication.clipboard().setText(self.input_text_edit.toPlainText()))
        copy_input_button.setStyleSheet("border: none;")

        # 创建清除按钮并连接清除功能
        pixmap_clear_button = QPixmap()
        pixmap_clear_button.loadFromData(QByteArray.fromHex(TUBIAO_clear_input_button))
        clear_input_button = QToolButton(self.input_text_edit)
        clear_input_button.setIcon(QIcon(pixmap_clear_button))
        clear_input_button.setToolTip("清除内容")
        clear_input_button.clicked.connect(lambda: self.input_text_edit.clear())
        clear_input_button.setStyleSheet("border: none;")

        # 创建按钮布局并添加工具按钮
        buttons_layout_input = QHBoxLayout()
        buttons_layout_input.addWidget(copy_input_button)
        buttons_layout_input.addWidget(clear_input_button)
        buttons_layout_input.setContentsMargins(0, 3, 3, 0)
        buttons_layout_input.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # 将按钮布局设置到输入文本框的布局中
        self.input_text_edit.setLayout(buttons_layout_input)
        layout.addWidget(self.input_text_edit)

        # 添加输出文本框和工具按钮
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setPlaceholderText("转换后的内容")
        self.output_text_edit.setStyleSheet("border: 1px solid gray;")

        # 创建工具按钮并连接复制功能
        pixmap_copy_button = QPixmap()
        pixmap_copy_button.loadFromData(QByteArray.fromHex(TUBIAO_copy_button))
        copy_output_button = QToolButton(self.output_text_edit)
        copy_output_button.setIcon(QIcon(pixmap_copy_button))  # 你可以替换为你的图标路径
        copy_output_button.setToolTip("复制内容")
        copy_output_button.clicked.connect(
            lambda: QApplication.clipboard().setText(self.output_text_edit.toPlainText()))
        copy_output_button.setStyleSheet("border: none;")

        # 创建清除按钮并连接清除功能
        pixmap_clear_button = QPixmap()
        pixmap_clear_button.loadFromData(QByteArray.fromHex(TUBIAO_clear_input_button))
        clear_output_button = QToolButton(self.output_text_edit)
        clear_output_button.setIcon(QIcon(pixmap_clear_button))  # 你可以替换为你的图标路径
        clear_output_button.setToolTip("清除内容")
        clear_output_button.clicked.connect(lambda: self.output_text_edit.clear())
        clear_output_button.setStyleSheet("border: none;")

        # 创建按钮布局并添加工具按钮
        buttons_layout_output = QHBoxLayout()
        buttons_layout_output.addWidget(copy_output_button)
        buttons_layout_output.addWidget(clear_output_button)
        buttons_layout_output.setContentsMargins(0, 3, 3, 0)
        buttons_layout_output.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # 将按钮布局设置到输出文本框的布局中
        self.output_text_edit.setLayout(buttons_layout_output)
        layout.addWidget(self.output_text_edit)

        # 添加按钮
        button_layout = QHBoxLayout()
        self.swap_button = QPushButton("互换")
        self.execute_button = QPushButton("执行")
        self.export_button = QPushButton("导出")

        self.swap_button.clicked.connect(self.swap_text)
        self.execute_button.clicked.connect(self.execute_encryption)
        self.export_button.clicked.connect(self.export_txt)

        button_layout.addWidget(self.swap_button)
        button_layout.addWidget(self.execute_button)
        button_layout.addWidget(self.export_button)

        Job_group_layout.addLayout(button_layout)

        # 添加选择加密文件按钮和编辑框
        select_file_button = QPushButton("选择加密文件")
        select_file_button.clicked.connect(self.select_encryption_file)
        layout.addWidget(select_file_button)

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("请选择加密文件路径")
        layout.addWidget(self.file_path_edit)

        # 初始化隐藏组件
        self.key_size_label.hide()
        self.key_size_2048.hide()
        self.key_size_3072.hide()
        self.key_size_4096.hide()
        self.key_size_custom.hide()
        self.generate_key_pair_button.hide()
        self.public_key_label.hide()
        self.private_key_label.hide()
        self.public_key_edit.hide()
        self.private_key_edit.hide()
        self.sha256_radio.hide()
        self.sha384_radio.hide()
        self.sha512_radio.hide()
        self.hash_function_label.hide()

        dialog.setLayout(layout)
        dialog.exec()

    def swap_text(self):
        text_edit_2_content = self.output_text_edit.toPlainText()
        self.input_text_edit.setPlainText(text_edit_2_content)
        self.output_text_edit.clear()
        # 切换当前操作
        if self.current_operation == "encrypt":
            self.current_operation = "decrypt"
        else:
            self.current_operation = "encrypt"

        # 根据当前操作设置加密和解密单选框的选择状态
        if self.current_operation == "encrypt":
            self.encryption_radio.setChecked(True)
            self.decryption_radio.setChecked(False)
        else:
            self.encryption_radio.setChecked(False)
            self.decryption_radio.setChecked(True)

    def export_txt(self):
        selected_method = self.encryption_combo_box.currentText()
        input_text = self.input_text_edit.toPlainText()
        output_text = self.output_text_edit.toPlainText()
        copied_text = ""
        # 根据不同的加密方式导出不同的内容
        if selected_method == "AES--对称加密":
            key = self.aes_key_edit.text()
            iv = self.iv_edit.text()
            encryption_mode = self.encryption_mode_combo_box.currentText()
            copied_text = f"KEY: {key}\nIV: {iv}\n加密方式: {selected_method}\n加密模式: {encryption_mode}\n加密前内容：{input_text}\n加密后内容：{output_text}"
        elif selected_method == "RSA--非对称加密":
            public_key = self.public_key_edit.text()
            private_key = self.private_key_edit.text()
            copied_text = f"Public Key: {public_key}\nPrivate Key: {private_key}\n加密方式: {selected_method}\n加密前内容：{input_text}\n加密后内容：{output_text}"
        elif selected_method == "SHA-XXX--哈希函数":
            if self.sha256_radio.isChecked():
                hash_method = "SHA-256"
            elif self.sha384_radio.isChecked():
                hash_method = "SHA-384"
            elif self.sha512_radio.isChecked():
                hash_method = "SHA-512"
            else:
                hash_method = "未选择"
            copied_text = f"哈希方式: {hash_method}\n哈希前内容：{input_text}\n哈希后内容：{output_text}"

        # 弹出窗口让用户选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(self.parent, "保存文件", "", "Text Files (*.txt)")

        if file_path:
            # 使用os模块获取文件路径
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)

            try:
                # 尝试打开文件进行写入
                with open(os.path.join(file_dir, file_name), 'w', encoding='utf-8') as file:
                    file.write(copied_text)
                QMessageBox.information(self.parent, "成功", "文件保存成功")
            except Exception as e:
                QMessageBox.critical(self.parent, "错误", f"无法保存文件：{str(e)}")

    def toggle_encryption_components(self):
        # 根据下拉框显示或隐藏内容
        if self.aes_key_label is None:
            return
        selected_method = self.encryption_combo_box.currentText()
        # 根据选择的加密方法来显示或隐藏相关组件
        if selected_method == "AES--对称加密":
            self.aes_key_label.show()
            self.aes_key_16.show()
            self.aes_key_24.show()
            self.aes_key_32.show()
            self.aes_key_edit.show()
            self.iv_label.show()
            self.iv_edit.show()
            self.random_key_button.show()
            self.encryption_mode_label.show()
            self.key_label.show()
            self.encryption_mode_combo_box.show()
            self.key_size_label.hide()
            self.key_size_2048.hide()
            self.key_size_3072.hide()
            self.key_size_4096.hide()
            self.key_size_custom.hide()
            self.generate_key_pair_button.hide()
            self.public_key_label.hide()
            self.private_key_label.hide()
            self.public_key_edit.hide()
            self.private_key_edit.hide()
            self.sha256_radio.hide()
            self.sha384_radio.hide()
            self.sha512_radio.hide()
            self.hash_function_label.hide()
            self.encryption_radio.show()
            self.decryption_radio.show()
            self.swap_button.show()
        elif selected_method == "RSA--非对称加密":
            self.aes_key_label.hide()
            self.aes_key_16.hide()
            self.aes_key_24.hide()
            self.aes_key_32.hide()
            self.aes_key_edit.hide()
            self.iv_label.hide()
            self.iv_edit.hide()
            self.random_key_button.hide()
            self.encryption_mode_label.hide()
            self.key_label.hide()
            self.encryption_mode_combo_box.hide()
            self.key_size_label.show()
            self.key_size_2048.show()
            self.key_size_3072.show()
            self.key_size_4096.show()
            self.key_size_custom.show()
            self.generate_key_pair_button.show()
            self.public_key_label.show()
            self.private_key_label.show()
            self.public_key_edit.show()
            self.private_key_edit.show()
            self.sha256_radio.hide()
            self.sha384_radio.hide()
            self.sha512_radio.hide()
            self.hash_function_label.hide()
            self.encryption_radio.show()
            self.decryption_radio.show()
            self.swap_button.show()
        elif selected_method == "SHA-XXX--哈希函数":
            self.aes_key_label.hide()
            self.aes_key_16.hide()
            self.aes_key_24.hide()
            self.aes_key_32.hide()
            self.aes_key_edit.hide()
            self.iv_label.hide()
            self.iv_edit.hide()
            self.random_key_button.hide()
            self.encryption_mode_label.hide()
            self.key_label.hide()
            self.encryption_mode_combo_box.hide()
            self.key_size_label.hide()
            self.key_size_2048.hide()
            self.key_size_3072.hide()
            self.key_size_4096.hide()
            self.key_size_custom.hide()
            self.generate_key_pair_button.hide()
            self.public_key_label.hide()
            self.private_key_label.hide()
            self.public_key_edit.hide()
            self.private_key_edit.hide()
            self.sha256_radio.show()
            self.sha384_radio.show()
            self.sha512_radio.show()
            self.hash_function_label.show()
            self.encryption_radio.hide()
            self.decryption_radio.hide()
            self.swap_button.hide()

    def generate_key_pair(self):
        try:
            # 检查用户选择的密钥大小
            if self.key_size_2048.isChecked():
                key_size = 2048
            elif self.key_size_3072.isChecked():
                key_size = 3072
            elif self.key_size_4096.isChecked():
                key_size = 4096
            else:
                # 如果用户选择了自定义大小，则获取自定义输入框中的值
                key_size = int(self.key_size_custom.text())

            # 生成 RSA 密钥对
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=default_backend()
            )

            # 获取公钥
            public_key = private_key.public_key()

            # 将密钥对序列化为PEM格式
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # 将生成的公钥和私钥显示在对应的文本框中
            self.public_key_edit.setText(public_key_pem.decode())
            self.private_key_edit.setText(private_key_pem.decode())

            QMessageBox.information(self.parent, "成功", "RSA 密钥对生成成功")

        except Exception as e:
            QMessageBox.critical(self.parent, "错误", f"生成密钥对失败：{str(e)}")

    def execute_encryption(self):
        try:
            # 执行按钮事件
            selected_method = self.encryption_combo_box.currentText()
            selected_mode = self.encryption_mode_combo_box.currentText()  # 获取所选的加密模式
            encryption_radio = self.encryption_radio.isChecked()
            decryption_radio = self.decryption_radio.isChecked()

            # 检查用户是否选择了文件或者输入了内容
            if not self.file_path_edit.text() and not self.input_text_edit.toPlainText() and not self.output_text_edit.toPlainText():
                QMessageBox.warning(self.parent, "警告", "请选择文件或输入内容")
                return

            # 生成随机 IV 并设置到编辑框中
            if encryption_radio and selected_mode != "ECB电子密码本模式":
                self.generate_random_iv()

            if selected_method == "AES--对称加密":
                key = self.aes_key_edit.text().encode()
                # 检查 AES 密钥是否为空
                if not key:
                    QMessageBox.warning(self.parent, "警告", "请输入 AES 密钥")
                    return

                if self.file_path_edit.text():
                    with open(self.file_path_edit.text(), 'rb') as file:
                        plaintext = file.read()
                else:
                    plaintext = self.input_text_edit.toPlainText().encode()

                if encryption_radio:
                    ciphertext = self.encrypt_aes(key, plaintext, selected_mode)
                    self.output_text_edit.setPlainText(ciphertext.hex())
                elif decryption_radio:
                    plaintext = self.decrypt_aes(key, bytes.fromhex(self.input_text_edit.toPlainText()), selected_mode)
                    self.output_text_edit.setPlainText(plaintext.decode())

            elif selected_method == "RSA--非对称加密":
                # 执行RSA非对称加密逻辑
                if encryption_radio:
                    if self.file_path_edit.text():  # 如果存在文件路径
                        # 读取文件内容
                        with open(self.file_path_edit.text(), 'rb') as file:
                            plaintext = file.read().decode('utf-8')
                        # 加密文件内容
                        ciphertext = self.encrypt_rsa(self.public_key_edit.text(), plaintext)
                        self.output_text_edit.setPlainText(ciphertext)
                    else:
                        ciphertext = self.encrypt_rsa(self.public_key_edit.text(), self.input_text_edit.toPlainText())
                        self.output_text_edit.setPlainText(ciphertext)
                elif decryption_radio:
                    plaintext = self.decrypt_rsa(self.private_key_edit.text(),
                                                 bytes.fromhex(self.input_text_edit.toPlainText()))
                    self.output_text_edit.setPlainText(plaintext)
            elif selected_method == "SHA-XXX--哈希函数":
                if self.sha256_radio.isChecked():
                    hash_algorithm = "sha256"
                elif self.sha384_radio.isChecked():
                    hash_algorithm = "sha384"
                elif self.sha512_radio.isChecked():
                    hash_algorithm = "sha512"
                else:
                    QMessageBox.warning(self.parent, "警告", "请选择哈希函数")
                    return

                if self.file_path_edit.text():
                    with open(self.file_path_edit.text(), 'rb') as file:
                        data = file.read()
                else:
                    data = self.input_text_edit.toPlainText().encode()

                hashed_data = self.generate_hash(hash_algorithm, data)
                self.output_text_edit.setPlainText(hashed_data.hex())

        except ValueError as ve:
            QMessageBox.warning(self.parent, "错误", str(ve))
        except Exception as e:
            QMessageBox.warning(self.parent, "错误", "发生未知错误：" + str(e))

    def generate_hash(self, algorithm, data):
        # 哈希值生成逻辑
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(data)
        return hash_obj.digest()

    def encrypt_aes(self, key, plaintext, mode):
        # AES加密
        try:
            if len(key) not in [16, 24, 32]:
                raise ValueError("AES 密钥长度必须为 16、24 或 32 字节")
            if mode == "ECB电子密码本模式":
                cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
            elif mode == "CBC密码分组链接模式":
                iv = bytes.fromhex(self.iv_edit.text())
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            elif mode == "CFB密码反馈模式":
                iv = bytes.fromhex(self.iv_edit.text())
                cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            elif mode == "OFB输出反馈模式":
                iv = bytes.fromhex(self.iv_edit.text())
                cipher = Cipher(algorithms.AES(key), modes.OFB(iv), backend=default_backend())
            elif mode == "CTR计数器模式":
                iv = bytes.fromhex(self.iv_edit.text())
                cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
            else:
                raise ValueError("Unsupported encryption mode")

            encryptor = cipher.encryptor()
            padder = hazmat.primitives.padding.PKCS7(algorithms.AES.block_size).padder()
            padded_plaintext = padder.update(plaintext) + padder.finalize()
            ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
            return ciphertext

        except Exception as e:
            raise ValueError("加密失败：" + str(e))

    def decrypt_aes(self, key, ciphertext, mode):
        # AES解密
        try:
            if len(key) not in [16, 24, 32]:
                raise ValueError("AES 密钥长度必须为 16、24 或 32 字节")
            if mode == "ECB电子密码本模式":
                cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
            elif mode == "CBC密码分组链接模式":
                iv = bytes.fromhex(self.iv_edit.text())
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            elif mode == "CFB密码反馈模式":
                iv = bytes.fromhex(self.iv_edit.text())
                cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            elif mode == "OFB输出反馈模式":
                iv = bytes.fromhex(self.iv_edit.text())
                cipher = Cipher(algorithms.AES(key), modes.OFB(iv), backend=default_backend())
            elif mode == "CTR计数器模式":
                iv = bytes.fromhex(self.iv_edit.text())
                cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
            else:
                raise ValueError("Unsupported encryption mode")

            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = hazmat.primitives.padding.PKCS7(algorithms.AES.block_size).unpadder()
            unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
            return unpadded_data

        except Exception as e:
            raise ValueError("解密失败：" + str(e))

    def encrypt_rsa(self, public_key_pem, plaintext):
        # RSA加密
        try:
            # 解码 PEM 格式的公钥
            public_key = serialization.load_pem_public_key(public_key_pem.encode(), backend=default_backend())

            # 使用 RSA 公钥加密数据
            ciphertext = public_key.encrypt(
                plaintext.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return ciphertext.hex()
        except Exception as e:
            raise ValueError("RSA加密失败：" + str(e))

    def decrypt_rsa(self, private_key_pem, ciphertext):
        # RSA解密
        try:
            # 解码 PEM 格式的私钥
            private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None,
                                                             backend=default_backend())

            # 使用 RSA 私钥解密数据
            plaintext = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return plaintext.decode()
        except Exception as e:
            raise ValueError("RSA解密失败：" + str(e))

    def generate_random_key(self):
        # 生成随机 KEY
        key_length = 8
        if self.aes_key_24.isChecked():
            key_length = 12
        elif self.aes_key_32.isChecked():
            key_length = 16
        random_content = os.urandom(key_length)
        key_hex = random_content.hex()
        self.aes_key_edit.setText(key_hex)

    def generate_random_iv(self):
        # 生成随机 IV
        iv = os.urandom(16)
        iv_hex = iv.hex()
        self.iv_edit.setText(iv_hex)

    def select_encryption_file(self):
        # 选择加密文件
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "选择加密文件", "", "All Files (*)")
        if file_path:
            self.file_path_edit.setText(file_path)

    def limit_aes_key_edit_length(self, length):
        # 限制KEY编辑框长度
        self.aes_key_edit.setMaxLength(length)
