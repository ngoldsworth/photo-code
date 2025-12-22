import subprocess
import pathlib as pl

# # subprocess.run(
# #     [
# #         r"C:\Program Files\Adobe\Adobe DNG Converter\Adobe DNG Converter.exe",
# #         # "-d", r"W:\NELSON\Desktop\test_converter",
# #         "-o ", r"\"W:\NELSON\Desktop\test_converter\test.dng\"",
# #         "-c",
# #         r"F:\DCIM\101NZ7_2\NCG_3481.NEF",
# #     ]
# # )

# p_adobe_dng_converter = pl.Path(
#     r"C:\Program Files\Adobe\Adobe DNG Converter\Adobe DNG Converter.exe"
# )
# src_dir = pl.Path(r"W:\NELSON\Desktop\test_converter\src")
# dst_dir = pl.Path(r"W:\NELSON\Desktop\test_converter\dst")

# for nef in src_dir.glob("*.NEF"):
#     print(nef)
#     cmd = [
#         '\"' + str(p_adobe_dng_converter) + '\"',
#         # f"-d \"{dst_dir}\"",
#         "-o \"test.dng\"",
#         f"-c \"{nef}\"",
#     ]
#     print(" ".join(cmd))
#     result = subprocess.run(cmd, check=True, shell=True)
#     print(result)

#     break

p_adobe_dng_converter = pl.Path(
    r"C:\Program Files\Adobe\Adobe DNG Converter\Adobe DNG Converter.exe"
)


def single_image_convert(input_file: pl.Path, output_dir: pl.Path):

    print(f"Processing: {input_file.name}")

    # Create a destination path for the new DNG file
    output_file = output_dir / f"{input_file.stem}.dng"

    # Build the command list with each argument as a separate string.
    # Do NOT add quotes. Do NOT use shell=True.
    cmd = [
        str(p_adobe_dng_converter),
        "-c",  # Use lossless compression
        "-o",
        str(output_file),  # Specify the full output file path
        str(input_file),  # The source file
    ]

    # print(f"Running command: {cmd}") # For debugging

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Successfully converted {input_file.name} to {output_file}")
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {input_file.name}.")
        print(f"Error: {e.stderr}")

    # break # Remove this line to process all files in the loop


src_dir = pl.Path(r"W:\NELSON\Desktop\test_converter\src")
dst_dir = pl.Path(r"W:\NELSON\Desktop\test_converter\dst")

if __name__ == "__main__":
    import multiprocessing as mp

    dst_dir.mkdir(exist_ok=True)

    for nef in src_dir.glob('*.NEF'):
        single_image_convert(nef, dst_dir)

    # with mp.Pool(4) as pool:
    #     # pool.starmap(single_image_convert, ({'input_file':inf, 'output_dir': dst_dir} for inf in src_dir.glob('*.NEF')))
    #     print('MADE IT HERE')
    #     for p in pool.starmap(single_image_convert, ((inf, dst_dir) for inf in src_dir.glob('*.NEF'))):
    #         print(p)


