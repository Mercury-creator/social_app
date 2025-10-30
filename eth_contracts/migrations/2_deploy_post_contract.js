// migrations/2_deploy_post_contract.js
const PostContract = artifacts.require("PostContract");

module.exports = function (deployer) {
  deployer.deploy(PostContract);
};