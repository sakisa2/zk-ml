nargo build
nargo execute
bb prove -b ./target/zk_ml.json -w ./target/zk_ml.gz -o ./target/
bb write_vk -b ./target/zk_ml.json -o target/
bb verify -k ./target/vk -p ./target/proof