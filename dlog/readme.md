# Dlog
A simple C++ streaming log library which has the same usage as ***glog***.

## Usage
now only support usages below:
- DLOG(INFO) << "content_need_to_log";
- DLOG(WARNING) << "content_need_to_log";
- DLOG(ERROR) << "content_need_to_log";
- DLOG(FATAL) << "content_need_to_log";
- DCHECK(expresson) << "content_need_to_log";
- DCHECK_NOT_NULL(ptr) << "content_need_to_log";

## Reference
- glog source code
