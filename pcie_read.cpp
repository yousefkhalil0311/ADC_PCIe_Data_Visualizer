#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <sstream>
#include <chrono>
#include <thread>
#include <fcntl.h>
#include <unistd.h>

using namespace std;

#define CHUNK_SIZE (1024)
#define NUM_CHUNKS 100

string generateFilename(int index){
    ostringstream oss;
    oss << "chunk_" << setfill('0') << setw(4) << index << ".bin";
    return oss.str();
}

int main(){

    ofstream ofs("/dev/shm/xdmaPythonStream", ios::binary);

    vector<uint16_t> buffer(CHUNK_SIZE);
    vector<uint32_t> outputbuffer(CHUNK_SIZE);

    int fd = open("/dev/xdma0_c2h_0", O_RDONLY);

    if(fd < 0) {perror("open"); return 1;}

    while(1){


        ssize_t bytes_read = read(fd, buffer.data(), CHUNK_SIZE * sizeof(uint16_t));

        if (bytes_read < 0) {
            perror("Read failed");
        } else if (bytes_read == 0) {
        printf("No data available (EOF or idle device)\n");
        } else {
            size_t words_read = bytes_read / sizeof(uint32_t);
            printf("Read %zd bytes (%zu words)\n", bytes_read, words_read);

            // Example: print first 4 values
            for (size_t i = 0; i < std::min(words_read, size_t(4)); ++i) {
                printf("buffer[%zu] = 0x%08X\n", i, buffer[i]);
            }
        }


        for(size_t i = 0; i < CHUNK_SIZE; i++){
            outputbuffer[i] = static_cast<uint32_t>(buffer[i]);
        }

        /*
        for(size_t i = 0; i < CHUNK_SIZE; i++){
            buffer[i] = static_cast<uint32_t>(i%256);
        }
            */

        ofs.write(reinterpret_cast<const char*>(buffer.data()), buffer.size());
    }

    close(fd);

    return 0;

    for(int chunkNum = 1; chunkNum <= NUM_CHUNKS; chunkNum++){
        string filename = generateFilename(chunkNum);

        ofstream ofs(filename, ios::binary);

        if(!ofs) {
            cerr << "Failed to open" << filename << "for writing.\n";
            return 1;
        }

        ofs.write(reinterpret_cast<const char*>(buffer.data()), buffer.size());

        if(!ofs) {
            cerr << "Failed to write to" << filename << "\n";
            return 1;
        }

        cout << "Wrote " << filename << "\n";

        this_thread::sleep_for(chrono::milliseconds(100));

    }

    return 0;
}

