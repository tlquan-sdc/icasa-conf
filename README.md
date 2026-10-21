# ICASA Conference Website

Website chính thức cho International Conference on AI-based Smart Agriculture in ASEAN (ICASA).

Đây là website tĩnh, không cần Node.js, PHP hoặc cơ sở dữ liệu. Microsoft CMT được sử dụng làm hệ thống nhận bài; website chỉ liên kết tới cổng CMT chính thức sau khi hội nghị được tạo.

## Chạy tại máy

```powershell
python -m http.server 8000
```

Mở `http://localhost:8000`.

## Cập nhật cho kỳ hội thảo mới

Tất cả dữ liệu thay đổi theo từng năm nằm trong `conference_config.py`, gồm:

- Năm và số thứ tự kỳ hội thảo.
- Thành phố, quốc gia, vùng, tọa độ và múi giờ.
- Thời gian nhận bài và tổ chức hội thảo.
- Đơn vị tổ chức và website chính thức.
- URL Microsoft CMT.
- Logo, ảnh hero và ảnh chia sẻ mạng xã hội.
- Các mốc thời gian và nhà tài trợ.

Sau khi sửa cấu hình, chạy:

```powershell
python build_site.py
```

Lệnh này tạo lại 8 trang HTML và `assets/site-data.js`. Không chỉnh trực tiếp các file HTML nếu muốn thay đổi được giữ lại sau lần build tiếp theo.

Khi đổi địa điểm vào năm sau, cần bổ sung ảnh hero mới vào `assets/`, sau đó cập nhật ít nhất các trường sau trong `conference_config.py`:

```python
"year": 2028,
"edition_number": "02",
"edition_ordinal": "2nd",
"edition_word": "second",
"edition_label": "Second edition",
"city": "New host city",
"country": "Host country",
"region": "Host region",
"latitude": "00.0000",
"longitude": "00.0000",
"setting": "Local setting",
"timezone": "Area/City",
"timezone_label": "UTC offset",
"hero_image": "assets/new-city-hero.webp",
"social_image": "assets/new-city-hero.webp",
"past_editions": [
    {"year": 2027, "url": "archive/2027/"},
],
```

Trước khi build kỳ 2028, hãy lưu nguyên website 2027 vào `archive/2027/`. Website 2028 vẫn chạy ở thư mục gốc, còn footer sẽ hiển thị `2028 Current edition` và liên kết `2027 archive`. Chỉ số như `02—08` trên đầu trang là vị trí trang trong hệ thống điều hướng, không phải số kỳ hội thảo hoặc năm tổ chức.

## Trước khi deploy

- Điền `site_url` bằng domain production để Open Graph sử dụng URL tuyệt đối.
- Điền `cmt_url` sau khi cổng Microsoft CMT được kích hoạt.
- Xác nhận ngày tổ chức, deadline, địa điểm, committee và keynote.
- Chỉ công bố thông tin xuất bản/indexing sau khi có xác nhận chính thức.
- Bổ sung email ban thư ký, chính sách riêng tư và điều khoản cần thiết.
- Xác nhận quyền sử dụng logo của các đơn vị liên quan.

## Bổ sung ảnh hội thảo

Không thêm ảnh trực tiếp vào HTML. Hãy tối ưu ảnh thật sang WebP, chép vào `assets/`, rồi khai báo trong danh sách `gallery` của `conference_config.py`:

```python
"gallery": [
    {
        "src": "assets/conference-opening.webp",
        "alt": "Delegates attending the ICASA opening session",
        "caption": "Opening session",
        "width": 1600,
        "height": 1067,
    },
],
```

Sau đó chạy `python build_site.py`. Gallery chỉ xuất hiện khi có ảnh trong danh sách; để trống thì toàn bộ khu vực này được ẩn. Nên dùng ảnh WebP rộng khoảng 1600 px, mỗi ảnh dưới 300 KB, mô tả `alt` đúng nội dung và chỉ đăng ảnh đã được phép sử dụng. Khi chuyển sang kỳ hội thảo năm sau, thay danh sách này bằng ảnh của kỳ mới.

## Deploy

Có thể deploy trực tiếp lên GitHub Pages, Netlify, Vercel hoặc bất kỳ dịch vụ hosting tĩnh nào. Publish directory là thư mục gốc chứa `index.html`.
