from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.db.dao.post_dao import PostDAO
from api.db.dao.user_dao import UserDAO
from api.web.api.post.schema import Post, PostCreate, PostID
from api.web.api.users.schema import AuthenticatedUser, UserBase
from api.libs.middleware.auth import is_authenticated

router = APIRouter()

"""
PostDAO側でユーザーの情報も取得してPostモデルに含めて返せばもっと簡潔なコードが書けるが
PostDAOがユーザーの情報にアクセスするは責務が増えることになってしまうのでここで別途取ってきて返す。
"""


@router.post("/create", response_model=Post)
async def add_post(
    post_create: PostCreate,
    user_info: AuthenticatedUser = Depends(is_authenticated),
    post_dao: PostDAO = Depends(),
) -> Post:
    """
    Creates a new post using the provided content and associates it with the authenticated user.

    Args:
        post_create (PostCreate): The schema containing the content of the post to be created.
        user_info (AuthenticatedUser): The authenticated user's information, obtained through dependency injection.
        post_dao (PostDAO): The Data Access Object for posts, obtained through dependency injection.

    Returns:
        Post: The created post, including its content, creation date, associated user, and statistics like favorite and repost counts.
    """
    post_data = await post_dao.create_post(
        userid=user_info.id,
        content=post_create.content
    )
    return Post(
        postid=post_data.postid,
        content=post_data.content,
        created_at=post_data.created_at,
        # Store user data within the Post data as well
        user=UserBase(
            id=user_info.id,
            username=user_info.username,
            userid=user_info.userid,
            icon=user_info.icon,
            header=user_info.header,
            profile=user_info.profile
        ),
        userid=post_data.userid,
        favorite_count=post_data.favorite_count,
        repost_count=post_data.repost_count
    )


@router.post("/show", response_model=Post)
async def get_post(
    post_id: PostID,
    post_dao: PostDAO = Depends(),
    user_dao: UserDAO = Depends(),
) -> Post:
    """
    Retrieves a post by its ID and includes user information associated with the post.

    Args:
        post_id (PostID): The ID of the post to retrieve.
        post_dao (PostDAO): The Data Access Object for posts, obtained through dependency injection.
        user_dao (UserDAO): The Data Access Object for users, obtained through dependency injection.

    Returns:
        Post: The post with the specified ID, including content, creation date, associated user, and statistics like favorite and repost counts.

    Raises:
        HTTPException: If the post with the specified ID is not found.
    """
    post_data = await post_dao.get_post_by_id(post_id.postid)

    if post_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post not found. Please check the post ID and try again."
        )

    # 返却するPostモデルにUserのデータが必要な為取ってくる
    user_info = await user_dao.get_user_by_id(post_data.userid)

    return Post(
        postid=post_data.postid,
        content=post_data.content,
        created_at=post_data.created_at,
        # Store user data within the Post data as well
        user=UserBase(
            id=user_info.id,
            username=user_info.username,
            userid=user_info.userid,
            icon=user_info.icon,
            header=user_info.header,
            profile=user_info.profile
        ),
        userid=post_data.userid,
        favorite_count=post_data.favorite_count,
        repost_count=post_data.repost_count
    )


@router.post("/delete")
async def delete_post(
    postid: PostID,
    post_dao: PostDAO = Depends(),
):
    post_data = await post_dao.get_post_by_id(postid)

    if post_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post not found. Please check the post ID and try again."
        )

    return await post_dao.delete_post(
        postid=postid.postid
    )


@router.get("/get-latest")
async def get_latest_post():
    return
