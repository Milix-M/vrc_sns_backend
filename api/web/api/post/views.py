from fastapi import APIRouter, Depends, HTTPException, status

from api.db.dao.post_dao import PostDAO
from api.db.dao.user_dao import UserDAO
from api.web.api.post.schema import Post, PostCreate, PostID
from api.web.api.users.schema import AuthenticatedUser, UserBase
from api.libs.middleware.auth import is_authenticated

router = APIRouter()


async def create_post_response(post_data: Post, user_info: UserBase) -> Post:
    """
    This function constructs a Post response model by combining the provided post data with user information.

    Although it would be more concise to have the PostDAO also fetch and include user information directly within the Post model,
    doing so would increase the responsibilities of PostDAO. Therefore, user information is fetched separately here and combined with the post data.

    Args:
        post_data (Post): The post data retrieved from the database.
        user_info (UserBase): The user information to be associated with the post.

    Returns:
        Post: A Post model populated with both post data and user information.
    """
    return Post(
        postid=post_data.postid,
        content=post_data.content,
        created_at=post_data.created_at,
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
    return await create_post_response(post_data, user_info)


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

    return await create_post_response(post_data, user_info)


@router.post("/delete")
async def delete_post(
    post_id: PostID,
    post_dao: PostDAO = Depends(),
) -> None:
    """
    Deletes a post by its ID.

    This endpoint allows you to delete a post specified by its ID. First, it checks if the post exists,
    If it does not exist, an HTTPException is sent indicating that the posting could not be found. If the post does exist
    delete the posting.

    Args:
        post_id (PostID): The ID of the post to delete.
        post_dao (PostDAO): The Data Access Object for posts, obtained through dependency injection.

    Raises:
        HTTPException: If the post with the specified ID is not found.
    """
    post_data = await post_dao.get_post_by_id(post_id.postid)

    if post_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post not found. Please check the post ID and try again."
        )

    return await post_dao.delete_post(
        postid=post_id.postid
    )
