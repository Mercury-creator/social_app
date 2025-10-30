// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;
pragma experimental ABIEncoderV2;

contract PostContract {
    struct Post {
        uint id;
        address author;
        string content;
    }

    Post[] public posts;

    event PostCreated(uint indexed id, address indexed author, string content);

    function createPost(string memory _content) public {
        uint postId = posts.length;
        posts.push(Post(postId, msg.sender, _content));

        emit PostCreated(postId, msg.sender, _content);
    }

    function getAllPosts() public view returns (Post[] memory) {
        return posts;
    }
    
    function getPostsCount() public view returns (uint256) {
        return posts.length;
    }
}
