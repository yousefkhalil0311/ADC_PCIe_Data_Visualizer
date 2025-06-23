#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <sstream>
#include <chrono>
#include <thread>

using namespace std;

#define CHUNK_SIZE (1024 * 1024)
#define NUM_CHUNKS 100

string generateFilename(int index){
    ostringstream oss;
    oss << "chunk_" << setfill('0') << setw(4) << index << ".bin";
    return oss.str();
}

int main(){
    vector<uint8_t> buffer(CHUNK_SIZE);
    
    for(size_t i = 0; i < CHUNK_SIZE; i++){
        buffer[i] = static_cast<uint8_t>(i%256);
    }

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

