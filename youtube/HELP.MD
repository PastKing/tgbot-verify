Liên kết YouTube hơi khác một chút, dạng như https://offers.sheerid.com/youtube/student/?yrdup=https%3A%2F%2Fwww.youtube.com%2F%3Fsld%3Dxxxxxxxxxxxxxxxytpid=premium&ytsku=premium&yrsp=https%3A%2F%2Fwww.youtube.com%2Fpremium%2FstudxxxxxxxxxxxxQQBRgO&euid=230493635&locale=en-US&oid=AI97cxxxxxxxxxxxxxxxxxxxxxNT06Nb5kDzo384b8cAu

Không có thông tin `programId` và `verificationId` của SheerID, nên bạn phải tự bắt request API.

Mở log mạng và tìm `https://services.sheerid.com/rest/v2/verification/`
Lấy `programId` trong payload và `verificationId` trong phản hồi

Ghép liên kết thủ công
https://services.sheerid.com/verify/xxxxxxxxxx/?verificationId=yyyyyyyyyyy
Trong đó `xxx` là `programId`
`yyyy` là `verificationId`