uv run main.py turntable --model-path data/ --output-dir output \
    --no-save-to-blend \
    --config.up "Y" \
    --config.forward "NEGATIVE_Z" \
    --config.camera-distance 2.5 \
    --config.camera-height 0.5 \
    --config.no-apply-default-material \
    --config.num-frames 30