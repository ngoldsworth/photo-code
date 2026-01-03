import pathlib as pl
import sqlite3
import multiprocessing
import time
import numpy as np
import io
from PIL import Image




QUEUE_MAXSIZE = 100
NUM_PROCS = 4


def reader(
    db: pl.Path, read_queue: multiprocessing.Queue, max_queue_size: int, num_procs: int
) -> None:
    for img in images_raw_iterator
        while read_queue.qsize() >= max_queue_size:
            time.sleep(1)
        read_queue.put(img)


    print("✅ All images queued.")


    # Signal end of stream to all processors
    for _ in range(num_procs):
        read_queue.put(None)




def raw_to_compressed_tiff(raw: bytes, w: int, h: int) -> bytes:
    """
    Converts raw RGB bytes to compressed TIFF bytes using Adobe Deflate.
    """
    arr = np.frombuffer(raw, dtype=np.uint8).reshape((h, w, 3))
    pil_img = Image.fromarray(arr)
    buffer = io.BytesIO()
    if OUT_FMT == 'tiff':
        if TIFF_COMPRESS:
            compression_method = 'tiff_lzw'
        else:
            compression_method = None
       
        pil_img.save(buffer, format="TIFF", compression=compression_method)
    elif OUT_FMT == 'png':
        pil_img.save(buffer, format="PNG")


    return buffer.getvalue()




def processor_worker(
    read_queue: multiprocessing.Queue,
    write_queue: multiprocessing.Queue,
) -> None:
    """
    Worker process that reads from read_queue, converts to TIFF, and pushes to write_queue.
    Exits when it receives None.
    """
    while True:
        try:
            item = read_queue.get(timeout=5)
            if item is None:
                print("🔚 Processor exiting.")
                break


            id, ts, w, h, raw_data = item
            tiff_bytes = raw_to_compressed_tiff(raw_data, w, h)
            write_queue.put((id, ts, tiff_bytes))


        except Exception as e:
            print(f"⚠️ Error processing image: {e}")




def writer(write_queue: multiprocessing.Queue, output_dir: pl.Path, count:int=0) -> None:
    """
    Writes TIFF bytes from write_queue to disk as .tiff files.
    Exits when it receives None.
    """
    if not output_dir.exists():
        output_dir.mkdir(parents=True)


    ct = 0
    while True:
        item = write_queue.get(timeout=60)
        if item is None:
            print("📝 Writer received shutdown signal.")
            break


        id, ts, tiff_bytes = item




        with open(output_dir / f"2002_{id:0>6}_{ts:0>13}.{OUT_FMT}", "wb") as f:
            f.write(tiff_bytes)


        if count > 0:
            ct += 1  
            if ct % 10 == 0:
                print(f'images completed: {ct:>6} of {count} ({ct/count:.2%})')




if __name__ == "__main__":


    read_queue: multiprocessing.Queue = multiprocessing.Queue(maxsize=QUEUE_MAXSIZE)
    write_queue: multiprocessing.Queue = multiprocessing.Queue(maxsize=QUEUE_MAXSIZE)


    # Start Reader
    reader_proc = multiprocessing.Process(
        target=reader, args=(db, read_queue, QUEUE_MAXSIZE, NUM_PROCS)
    )
    reader_proc.start()


    # Start Processor Workers
    processors = []
    for j in range(NUM_PROCS):
        proc = multiprocessing.Process(
            target=processor_worker, args=(read_queue, write_queue)
        )
        proc.start()
        print(f"🚀 Processor {j} started.")
        processors.append(proc)


    # Start Writer
    writer_proc = multiprocessing.Process(target=writer, args=(write_queue, DST, img_count))
    writer_proc.start()


    print(f"✅ Pipeline is running with {NUM_PROCS} processors.")


    try:
        # Wait for reader to finish
        reader_proc.join()
        print("📥 Reader exited.")


        # Wait for all processors to finish
        for j, proc in enumerate(processors):
            proc.join()
            print(f"⚙️  Processor {j} exited.")


        # Signal writer to shut down
        write_queue.put(None)


        # Wait for writer to finish
        writer_proc.join()
        print("📝 Writer exited.")
        print("✅ Pipeline complete and cleanly shut down.")


    except KeyboardInterrupt:
        print("🛑 Ctrl+C caught. Terminating processes...")
        reader_proc.terminate()
        for proc in processors:
            proc.terminate()
        writer_proc.terminate()
        print("☠️ Force shutdown complete.")




