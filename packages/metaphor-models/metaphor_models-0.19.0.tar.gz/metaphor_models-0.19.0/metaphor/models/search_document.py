from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Any, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class AnchorEntityType(Enum):
    DASHBOARD = "DASHBOARD"
    DATASET = "DATASET"
    DATA_DOCUMENT = "DATA_DOCUMENT"
    DBT_MODEL = "DBT_MODEL"
    LOOKER_EXPLORE = "LOOKER_EXPLORE"
    LOOKER_VIEW = "LOOKER_VIEW"
    METRIC = "METRIC"
    POWER_BI_DATASET = "POWER_BI_DATASET"
    TABLEAU_DATASOURCE = "TABLEAU_DATASOURCE"
    THOUGHT_SPOT_DATA_OBJECT = "THOUGHT_SPOT_DATA_OBJECT"


@dataclass
class Highlight:
    """Used in search response, highlight the section where the match happens"""
    chart_descriptions: Optional[List[str]] = None
    charts: Optional[List[str]] = None
    contact_display_names: Optional[List[str]] = None
    dashboard_id: Optional[str] = None
    description: Optional[str] = None
    governed_tags: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    name: Optional[str] = None
    column_descriptions: Optional[List[str]] = None
    column_names: Optional[List[str]] = None
    column_tags: Optional[List[str]] = None
    author_display_name: Optional[str] = None
    content: Optional[str] = None
    column: Optional[str] = None
    email: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Highlight':
        assert isinstance(obj, dict)
        chart_descriptions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("chartDescriptions"))
        charts = from_union([lambda x: from_list(from_str, x), from_none], obj.get("charts"))
        contact_display_names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("contactDisplayNames"))
        dashboard_id = from_union([from_str, from_none], obj.get("dashboardId"))
        description = from_union([from_none, from_str], obj.get("description"))
        governed_tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("governedTags"))
        hashtags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("hashtags"))
        name = from_union([from_str, from_none], obj.get("name"))
        column_descriptions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("columnDescriptions"))
        column_names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("columnNames"))
        column_tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("columnTags"))
        author_display_name = from_union([from_str, from_none], obj.get("authorDisplayName"))
        content = from_union([from_str, from_none], obj.get("content"))
        column = from_union([from_str, from_none], obj.get("column"))
        email = from_union([from_str, from_none], obj.get("email"))
        return Highlight(chart_descriptions, charts, contact_display_names, dashboard_id, description, governed_tags, hashtags, name, column_descriptions, column_names, column_tags, author_display_name, content, column, email)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.chart_descriptions is not None:
            result["chartDescriptions"] = from_union([lambda x: from_list(from_str, x), from_none], self.chart_descriptions)
        if self.charts is not None:
            result["charts"] = from_union([lambda x: from_list(from_str, x), from_none], self.charts)
        if self.contact_display_names is not None:
            result["contactDisplayNames"] = from_union([lambda x: from_list(from_str, x), from_none], self.contact_display_names)
        if self.dashboard_id is not None:
            result["dashboardId"] = from_union([from_str, from_none], self.dashboard_id)
        if self.description is not None:
            result["description"] = from_union([from_none, from_str], self.description)
        if self.governed_tags is not None:
            result["governedTags"] = from_union([lambda x: from_list(from_str, x), from_none], self.governed_tags)
        if self.hashtags is not None:
            result["hashtags"] = from_union([lambda x: from_list(from_str, x), from_none], self.hashtags)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.column_descriptions is not None:
            result["columnDescriptions"] = from_union([lambda x: from_list(from_str, x), from_none], self.column_descriptions)
        if self.column_names is not None:
            result["columnNames"] = from_union([lambda x: from_list(from_str, x), from_none], self.column_names)
        if self.column_tags is not None:
            result["columnTags"] = from_union([lambda x: from_list(from_str, x), from_none], self.column_tags)
        if self.author_display_name is not None:
            result["authorDisplayName"] = from_union([from_str, from_none], self.author_display_name)
        if self.content is not None:
            result["content"] = from_union([from_str, from_none], self.content)
        if self.column is not None:
            result["column"] = from_union([from_str, from_none], self.column)
        if self.email is not None:
            result["email"] = from_union([from_str, from_none], self.email)
        return result


class Platform(Enum):
    BIGQUERY = "BIGQUERY"
    DOCUMENTDB = "DOCUMENTDB"
    DYNAMODB = "DYNAMODB"
    ELASTICSEARCH = "ELASTICSEARCH"
    EXTERNAL = "EXTERNAL"
    GLUE = "GLUE"
    LOOKER = "LOOKER"
    METABASE = "METABASE"
    MSSQL = "MSSQL"
    MYSQL = "MYSQL"
    POSTGRESQL = "POSTGRESQL"
    POWER_BI = "POWER_BI"
    RDS = "RDS"
    REDIS = "REDIS"
    REDSHIFT = "REDSHIFT"
    S3 = "S3"
    SNOWFLAKE = "SNOWFLAKE"
    SYNAPSE = "SYNAPSE"
    TABLEAU = "TABLEAU"
    THOUGHT_SPOT = "THOUGHT_SPOT"
    UNITY_CATALOG = "UNITY_CATALOG"
    UNKNOWN = "UNKNOWN"


@dataclass
class QueryCountPercentile:
    last24_hours: Optional[float] = None
    last30_days: Optional[float] = None
    last365_days: Optional[float] = None
    last7_days: Optional[float] = None
    last90_days: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'QueryCountPercentile':
        assert isinstance(obj, dict)
        last24_hours = from_union([from_float, from_none], obj.get("last24Hours"))
        last30_days = from_union([from_float, from_none], obj.get("last30Days"))
        last365_days = from_union([from_float, from_none], obj.get("last365Days"))
        last7_days = from_union([from_float, from_none], obj.get("last7Days"))
        last90_days = from_union([from_float, from_none], obj.get("last90Days"))
        return QueryCountPercentile(last24_hours, last30_days, last365_days, last7_days, last90_days)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.last24_hours is not None:
            result["last24Hours"] = from_union([to_float, from_none], self.last24_hours)
        if self.last30_days is not None:
            result["last30Days"] = from_union([to_float, from_none], self.last30_days)
        if self.last365_days is not None:
            result["last365Days"] = from_union([to_float, from_none], self.last365_days)
        if self.last7_days is not None:
            result["last7Days"] = from_union([to_float, from_none], self.last7_days)
        if self.last90_days is not None:
            result["last90Days"] = from_union([to_float, from_none], self.last90_days)
        return result


@dataclass
class SearchScoreDetails:
    description: Optional[str] = None
    details: Optional[List['SearchScoreDetails']] = None
    value: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SearchScoreDetails':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        details = from_union([lambda x: from_list(SearchScoreDetails.from_dict, x), from_none], obj.get("details"))
        value = from_union([from_float, from_none], obj.get("value"))
        return SearchScoreDetails(description, details, value)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.description is not None:
            result["description"] = from_union([from_str, from_none], self.description)
        if self.details is not None:
            result["details"] = from_union([lambda x: from_list(lambda x: to_class(SearchScoreDetails, x), x), from_none], self.details)
        if self.value is not None:
            result["value"] = from_union([to_float, from_none], self.value)
        return result


class ThoughtSpotDashboardType(Enum):
    ANSWER = "ANSWER"
    LIVEBOARD = "LIVEBOARD"
    UNKNOWN = "UNKNOWN"


class ThoughtSpotDataObjectType(Enum):
    TABLE = "TABLE"
    UNKNOWN = "UNKNOWN"
    VIEW = "VIEW"
    WORKSHEET = "WORKSHEET"


class TypeEnum(Enum):
    ASSET_CONTACT = "ASSET_CONTACT"
    ASSET_DESCRIPTION = "ASSET_DESCRIPTION"
    CHANGE_REQUEST = "CHANGE_REQUEST"
    COLUMN_DESCRIPTION = "COLUMN_DESCRIPTION"
    COMMENT = "COMMENT"
    COMMON_COLUMN_DESCRIPTION = "COMMON_COLUMN_DESCRIPTION"
    DATA_DOCUMENT = "DATA_DOCUMENT"
    DATA_GROUP = "DATA_GROUP"
    DATA_UNIT = "DATA_UNIT"
    DBT_METRIC = "DBT_METRIC"
    DBT_MODEL = "DBT_MODEL"
    DEPRECATION = "DEPRECATION"
    GOVERNED_TAG = "GOVERNED_TAG"
    HOW_TO_USE = "HOW_TO_USE"
    INCIDENT = "INCIDENT"
    LOOKER_EXPLORE = "LOOKER_EXPLORE"
    LOOKER_VIEW = "LOOKER_VIEW"
    PERSONAL_SPACE = "PERSONAL_SPACE"
    POWER_BI_DATASET = "POWER_BI_DATASET"
    TABLEAU_DATASOURCE = "TABLEAU_DATASOURCE"
    THOUGHT_SPOT_DATA_OBJECT = "THOUGHT_SPOT_DATA_OBJECT"
    UNKNOWN = "UNKNOWN"
    USER_DEFINED_SPACE = "USER_DEFINED_SPACE"


class VirtualViewType(Enum):
    DBT_MODEL = "DBT_MODEL"
    LOOKER_EXPLORE = "LOOKER_EXPLORE"
    LOOKER_VIEW = "LOOKER_VIEW"
    POWER_BI_DATASET = "POWER_BI_DATASET"
    TABLEAU_DATASOURCE = "TABLEAU_DATASOURCE"
    THOUGHT_SPOT_DATA_OBJECT = "THOUGHT_SPOT_DATA_OBJECT"
    UNKNOWN = "UNKNOWN"


@dataclass
class SearchDocument:
    browse_path_hierarchy: Optional[List[str]] = None
    browse_paths: Optional[List[str]] = None
    browse_path_segments: Optional[List[str]] = None
    chart_descriptions: Optional[List[str]] = None
    charts: Optional[List[str]] = None
    contact_display_names: Optional[List[str]] = None
    dashboard_id: Optional[str] = None
    description: Optional[str] = None
    document_id: Optional[str] = None
    entity_id: Optional[str] = None
    governed_tags: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    """Used in search response, highlight the section where the match happens"""
    highlight: Optional[Highlight] = None
    is_deleted: Optional[bool] = None
    knowledge_card_count: Optional[float] = None
    last_refreshed: Optional[datetime] = None
    model: Optional[str] = None
    """Name of the related entity"""
    name: Optional[str] = None
    platform: Optional[Platform] = None
    project: Optional[str] = None
    score_details: Optional[SearchScoreDetails] = None
    thought_spot_dashboard_type: Optional[ThoughtSpotDashboardType] = None
    view_count: Optional[float] = None
    workspace: Optional[str] = None
    column_descriptions: Optional[List[str]] = None
    column_names: Optional[List[str]] = None
    column_tags: Optional[List[str]] = None
    database: Optional[str] = None
    materialization_type: Optional[str] = None
    query_count_percentile: Optional[QueryCountPercentile] = None
    row_count: Optional[float] = None
    schema: Optional[str] = None
    size: Optional[float] = None
    usage_level: Optional[str] = None
    usage_percentile: Optional[float] = None
    anchor_entity_id: Optional[str] = None
    anchor_entity_type: Optional[AnchorEntityType] = None
    author: Optional[str] = None
    author_display_name: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[str] = None
    directory: Optional[List[str]] = None
    is_archived: Optional[bool] = None
    is_draft: Optional[bool] = None
    type: Optional[TypeEnum] = None
    tags: Optional[List[str]] = None
    thought_spot_data_object_type: Optional[ThoughtSpotDataObjectType] = None
    column: Optional[str] = None
    column_description: Optional[str] = None
    virtual_view_type: Optional[VirtualViewType] = None
    department: Optional[str] = None
    email: Optional[str] = None
    skills: Optional[List[str]] = None
    title: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SearchDocument':
        assert isinstance(obj, dict)
        browse_path_hierarchy = from_union([lambda x: from_list(from_str, x), from_none], obj.get("browsePathHierarchy"))
        browse_paths = from_union([lambda x: from_list(from_str, x), from_none], obj.get("browsePaths"))
        browse_path_segments = from_union([lambda x: from_list(from_str, x), from_none], obj.get("browsePathSegments"))
        chart_descriptions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("chartDescriptions"))
        charts = from_union([lambda x: from_list(from_str, x), from_none], obj.get("charts"))
        contact_display_names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("contactDisplayNames"))
        dashboard_id = from_union([from_str, from_none], obj.get("dashboardId"))
        description = from_union([from_none, from_str], obj.get("description"))
        document_id = from_union([from_str, from_none], obj.get("documentId"))
        entity_id = from_union([from_str, from_none], obj.get("entityId"))
        governed_tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("governedTags"))
        hashtags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("hashtags"))
        highlight = from_union([Highlight.from_dict, from_none], obj.get("highlight"))
        is_deleted = from_union([from_bool, from_none], obj.get("isDeleted"))
        knowledge_card_count = from_union([from_float, from_none], obj.get("knowledgeCardCount"))
        last_refreshed = from_union([from_datetime, from_none], obj.get("lastRefreshed"))
        model = from_union([from_none, from_str], obj.get("model"))
        name = from_union([from_str, from_none], obj.get("name"))
        platform = from_union([Platform, from_none], obj.get("platform"))
        project = from_union([from_none, from_str], obj.get("project"))
        score_details = from_union([SearchScoreDetails.from_dict, from_none], obj.get("scoreDetails"))
        thought_spot_dashboard_type = from_union([from_none, ThoughtSpotDashboardType], obj.get("thoughtSpotDashboardType"))
        view_count = from_union([from_float, from_none], obj.get("viewCount"))
        workspace = from_union([from_none, from_str], obj.get("workspace"))
        column_descriptions = from_union([lambda x: from_list(from_str, x), from_none], obj.get("columnDescriptions"))
        column_names = from_union([lambda x: from_list(from_str, x), from_none], obj.get("columnNames"))
        column_tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("columnTags"))
        database = from_union([from_str, from_none], obj.get("database"))
        materialization_type = from_union([from_none, from_str], obj.get("materializationType"))
        query_count_percentile = from_union([QueryCountPercentile.from_dict, from_none], obj.get("queryCountPercentile"))
        row_count = from_union([from_float, from_none], obj.get("rowCount"))
        schema = from_union([from_str, from_none], obj.get("schema"))
        size = from_union([from_float, from_none], obj.get("size"))
        usage_level = from_union([from_str, from_none], obj.get("usageLevel"))
        usage_percentile = from_union([from_float, from_none], obj.get("usagePercentile"))
        anchor_entity_id = from_union([from_none, from_str], obj.get("anchorEntityId"))
        anchor_entity_type = from_union([from_none, AnchorEntityType], obj.get("anchorEntityType"))
        author = from_union([from_none, from_str], obj.get("author"))
        author_display_name = from_union([from_none, from_str], obj.get("authorDisplayName"))
        content = from_union([from_none, from_str], obj.get("content"))
        created_at = from_union([from_none, from_str], obj.get("createdAt"))
        directory = from_union([lambda x: from_list(from_str, x), from_none], obj.get("directory"))
        is_archived = from_union([from_bool, from_none], obj.get("isArchived"))
        is_draft = from_union([from_bool, from_none], obj.get("isDraft"))
        type = from_union([TypeEnum, from_none], obj.get("type"))
        tags = from_union([lambda x: from_list(from_str, x), from_none], obj.get("tags"))
        thought_spot_data_object_type = from_union([from_none, ThoughtSpotDataObjectType], obj.get("thoughtSpotDataObjectType"))
        column = from_union([from_str, from_none], obj.get("column"))
        column_description = from_union([from_none, from_str], obj.get("columnDescription"))
        virtual_view_type = from_union([VirtualViewType, from_none], obj.get("virtualViewType"))
        department = from_union([from_none, from_str], obj.get("department"))
        email = from_union([from_str, from_none], obj.get("email"))
        skills = from_union([lambda x: from_list(from_str, x), from_none], obj.get("skills"))
        title = from_union([from_none, from_str], obj.get("title"))
        return SearchDocument(browse_path_hierarchy, browse_paths, browse_path_segments, chart_descriptions, charts, contact_display_names, dashboard_id, description, document_id, entity_id, governed_tags, hashtags, highlight, is_deleted, knowledge_card_count, last_refreshed, model, name, platform, project, score_details, thought_spot_dashboard_type, view_count, workspace, column_descriptions, column_names, column_tags, database, materialization_type, query_count_percentile, row_count, schema, size, usage_level, usage_percentile, anchor_entity_id, anchor_entity_type, author, author_display_name, content, created_at, directory, is_archived, is_draft, type, tags, thought_spot_data_object_type, column, column_description, virtual_view_type, department, email, skills, title)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.browse_path_hierarchy is not None:
            result["browsePathHierarchy"] = from_union([lambda x: from_list(from_str, x), from_none], self.browse_path_hierarchy)
        if self.browse_paths is not None:
            result["browsePaths"] = from_union([lambda x: from_list(from_str, x), from_none], self.browse_paths)
        if self.browse_path_segments is not None:
            result["browsePathSegments"] = from_union([lambda x: from_list(from_str, x), from_none], self.browse_path_segments)
        if self.chart_descriptions is not None:
            result["chartDescriptions"] = from_union([lambda x: from_list(from_str, x), from_none], self.chart_descriptions)
        if self.charts is not None:
            result["charts"] = from_union([lambda x: from_list(from_str, x), from_none], self.charts)
        if self.contact_display_names is not None:
            result["contactDisplayNames"] = from_union([lambda x: from_list(from_str, x), from_none], self.contact_display_names)
        if self.dashboard_id is not None:
            result["dashboardId"] = from_union([from_str, from_none], self.dashboard_id)
        if self.description is not None:
            result["description"] = from_union([from_none, from_str], self.description)
        if self.document_id is not None:
            result["documentId"] = from_union([from_str, from_none], self.document_id)
        if self.entity_id is not None:
            result["entityId"] = from_union([from_str, from_none], self.entity_id)
        if self.governed_tags is not None:
            result["governedTags"] = from_union([lambda x: from_list(from_str, x), from_none], self.governed_tags)
        if self.hashtags is not None:
            result["hashtags"] = from_union([lambda x: from_list(from_str, x), from_none], self.hashtags)
        if self.highlight is not None:
            result["highlight"] = from_union([lambda x: to_class(Highlight, x), from_none], self.highlight)
        if self.is_deleted is not None:
            result["isDeleted"] = from_union([from_bool, from_none], self.is_deleted)
        if self.knowledge_card_count is not None:
            result["knowledgeCardCount"] = from_union([to_float, from_none], self.knowledge_card_count)
        if self.last_refreshed is not None:
            result["lastRefreshed"] = from_union([lambda x: x.isoformat(), from_none], self.last_refreshed)
        if self.model is not None:
            result["model"] = from_union([from_none, from_str], self.model)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.platform is not None:
            result["platform"] = from_union([lambda x: to_enum(Platform, x), from_none], self.platform)
        if self.project is not None:
            result["project"] = from_union([from_none, from_str], self.project)
        if self.score_details is not None:
            result["scoreDetails"] = from_union([lambda x: to_class(SearchScoreDetails, x), from_none], self.score_details)
        if self.thought_spot_dashboard_type is not None:
            result["thoughtSpotDashboardType"] = from_union([from_none, lambda x: to_enum(ThoughtSpotDashboardType, x)], self.thought_spot_dashboard_type)
        if self.view_count is not None:
            result["viewCount"] = from_union([to_float, from_none], self.view_count)
        if self.workspace is not None:
            result["workspace"] = from_union([from_none, from_str], self.workspace)
        if self.column_descriptions is not None:
            result["columnDescriptions"] = from_union([lambda x: from_list(from_str, x), from_none], self.column_descriptions)
        if self.column_names is not None:
            result["columnNames"] = from_union([lambda x: from_list(from_str, x), from_none], self.column_names)
        if self.column_tags is not None:
            result["columnTags"] = from_union([lambda x: from_list(from_str, x), from_none], self.column_tags)
        if self.database is not None:
            result["database"] = from_union([from_str, from_none], self.database)
        if self.materialization_type is not None:
            result["materializationType"] = from_union([from_none, from_str], self.materialization_type)
        if self.query_count_percentile is not None:
            result["queryCountPercentile"] = from_union([lambda x: to_class(QueryCountPercentile, x), from_none], self.query_count_percentile)
        if self.row_count is not None:
            result["rowCount"] = from_union([to_float, from_none], self.row_count)
        if self.schema is not None:
            result["schema"] = from_union([from_str, from_none], self.schema)
        if self.size is not None:
            result["size"] = from_union([to_float, from_none], self.size)
        if self.usage_level is not None:
            result["usageLevel"] = from_union([from_str, from_none], self.usage_level)
        if self.usage_percentile is not None:
            result["usagePercentile"] = from_union([to_float, from_none], self.usage_percentile)
        if self.anchor_entity_id is not None:
            result["anchorEntityId"] = from_union([from_none, from_str], self.anchor_entity_id)
        if self.anchor_entity_type is not None:
            result["anchorEntityType"] = from_union([from_none, lambda x: to_enum(AnchorEntityType, x)], self.anchor_entity_type)
        if self.author is not None:
            result["author"] = from_union([from_none, from_str], self.author)
        if self.author_display_name is not None:
            result["authorDisplayName"] = from_union([from_none, from_str], self.author_display_name)
        if self.content is not None:
            result["content"] = from_union([from_none, from_str], self.content)
        if self.created_at is not None:
            result["createdAt"] = from_union([from_none, from_str], self.created_at)
        if self.directory is not None:
            result["directory"] = from_union([lambda x: from_list(from_str, x), from_none], self.directory)
        if self.is_archived is not None:
            result["isArchived"] = from_union([from_bool, from_none], self.is_archived)
        if self.is_draft is not None:
            result["isDraft"] = from_union([from_bool, from_none], self.is_draft)
        if self.type is not None:
            result["type"] = from_union([lambda x: to_enum(TypeEnum, x), from_none], self.type)
        if self.tags is not None:
            result["tags"] = from_union([lambda x: from_list(from_str, x), from_none], self.tags)
        if self.thought_spot_data_object_type is not None:
            result["thoughtSpotDataObjectType"] = from_union([from_none, lambda x: to_enum(ThoughtSpotDataObjectType, x)], self.thought_spot_data_object_type)
        if self.column is not None:
            result["column"] = from_union([from_str, from_none], self.column)
        if self.column_description is not None:
            result["columnDescription"] = from_union([from_none, from_str], self.column_description)
        if self.virtual_view_type is not None:
            result["virtualViewType"] = from_union([lambda x: to_enum(VirtualViewType, x), from_none], self.virtual_view_type)
        if self.department is not None:
            result["department"] = from_union([from_none, from_str], self.department)
        if self.email is not None:
            result["email"] = from_union([from_str, from_none], self.email)
        if self.skills is not None:
            result["skills"] = from_union([lambda x: from_list(from_str, x), from_none], self.skills)
        if self.title is not None:
            result["title"] = from_union([from_none, from_str], self.title)
        return result


def search_document_from_dict(s: Any) -> SearchDocument:
    return SearchDocument.from_dict(s)


def search_document_to_dict(x: SearchDocument) -> Any:
    return to_class(SearchDocument, x)
