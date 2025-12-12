export OPENCV_IO_ENABLE_OPENEXR=1
export OUTPUT_FOLDER=/data/jwb/Hunyuan3D-2.1/hy3dshape/tools/example_output
export BLENDER_PATH=/data/jwb/Hunyuan3D-2.1/blender-4.5.3-linux-x64/blender

export INPUT_FILE=/data/jwb/Hunyuan3D-2.1/hy3dshape/tools/example_glb/Msh_BathroomSink.glb
export NAME=example

$BLENDER_PATH -b -P render/render.py -- --object ${INPUT_FILE} --output_folder $OUTPUT_FOLDER/$NAME/render_cond --geo_mode --resolution 512
# $BLENDER_PATH -b -P render/render.py -- --object ${INPUT_FILE} --output_folder $OUTPUT_FOLDER/$NAME/render_tex --resolution 512
python3 watertight/watertight_and_sample.py --input_obj $OUTPUT_FOLDER/$NAME/render_cond/mesh.ply --output_prefix $OUTPUT_FOLDER/$NAME/geo_data/$NAME
