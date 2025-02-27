// ----------------------------------------------------------------------------
// -                        Open3D: www.open3d.org                            -
// ----------------------------------------------------------------------------
// The MIT License (MIT)
//
// Copyright (c) 2018-2021 www.open3d.org
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
// IN THE SOFTWARE.
// ----------------------------------------------------------------------------

#include "open3d/data/Extract.h"

#include "open3d/data/Dataset.h"
#include "open3d/data/Download.h"
#include "open3d/utility/FileSystem.h"
#include "tests/Tests.h"

namespace open3d {
namespace tests {

TEST(Extract, ExtractFromZIP) {
    // Directory relative to `data_root`, where files will be temp. downloaded
    // for this test.
    const std::string prefix = "open3d_tmp/test_extract";
    const std::string extract_dir = data::LocateDataRoot() + "/" + prefix;
    EXPECT_TRUE(utility::filesystem::DeleteDirectory(extract_dir));

    // Download the `test_data_00.zip` test data.
    std::string url =
            "https://github.com/isl-org/open3d_downloads/releases/download/"
            "data-manager/test_data_00.zip";
    std::string md5 = "996987b27c4497dbb951ec056c9684f4";
    std::string file_path = extract_dir + "/test_data_00.zip";
    // This download shall work.
    EXPECT_EQ(data::DownloadFromURL(url, md5, prefix), file_path);

    // Extract the test zip file.
    EXPECT_NO_THROW(data::Extract(file_path, extract_dir));
    std::string output_file = extract_dir + "/test_data/lena_color.jpg";
    // Check if the extracted file exists.
    EXPECT_TRUE(utility::filesystem::FileExists(output_file));

    // Download the `test_data_00.tar.xy` test data.
    url = "https://github.com/isl-org/open3d_downloads/releases/download/"
          "data-manager/test_data_00.tar.xz";
    md5 = "61dec8a20bfe288f0bfa7cb38597587f";
    file_path = extract_dir + "/test_data_00.tar.xz";
    EXPECT_EQ(data::DownloadFromURL(url, md5, prefix), file_path);

    // Currently only `.zip` files are supported.
    EXPECT_ANY_THROW(data::Extract(file_path, extract_dir));

    // Clean up.
    EXPECT_TRUE(utility::filesystem::DeleteDirectory(extract_dir));
}

}  // namespace tests
}  // namespace open3d
