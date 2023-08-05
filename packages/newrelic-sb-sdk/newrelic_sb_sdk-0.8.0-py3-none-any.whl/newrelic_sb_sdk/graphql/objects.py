__all__ = [
    "AiIssuesIIncident",
    "AiWorkflowsResponseError",
    "AlertableEntity",
    "AlertableEntityOutline",
    "AlertsNotificationChannel",
    "AlertsNrqlCondition",
    "ApiAccessKey",
    "ApiAccessKeyError",
    "ApmBrowserApplicationEntity",
    "ApmBrowserApplicationEntityOutline",
    "CloudIntegration",
    "CloudProvider",
    "CollectionEntity",
    "EdgeEndpointDetail",
    "EntityRelationshipEdge",
    "ErrorsInboxResource",
    "ErrorsInboxResponseError",
    "InfrastructureIntegrationEntity",
    "InfrastructureIntegrationEntityOutline",
    "Nr1CatalogInstallPlanDirective",
    "Nr1CatalogInstaller",
    "Nr1CatalogNerdpackItem",
    "Nr1CatalogNerdpackItemMetadata",
    "Nr1CatalogPreview",
    "Nr1CatalogQuickstartComponent",
    "Nr1CatalogQuickstartComponentMetadata",
    "Nr1CatalogSupportedEntityTypes",
    "SuggestedNrqlQuery",
    "WhatsNewContent",
    "WorkloadStatusResult",
    "Entity",
    "EntityOutline",
    "Account",
    "AccountManagementCreateResponse",
    "AccountManagementManagedAccount",
    "AccountManagementOrganizationStitchedFields",
    "AccountManagementUpdateResponse",
    "AccountOutline",
    "AccountReference",
    "Actor",
    "AgentApplicationApmBrowserSettings",
    "AgentApplicationBrowserSettings",
    "AgentApplicationCreateBrowserResult",
    "AgentApplicationCreateMobileResult",
    "AgentApplicationDeleteResult",
    "AgentApplicationEnableBrowserResult",
    "AgentApplicationSettingsApmBase",
    "AgentApplicationSettingsApmConfig",
    "AgentApplicationSettingsBrowserAjax",
    "AgentApplicationSettingsBrowserBase",
    "AgentApplicationSettingsBrowserConfig",
    "AgentApplicationSettingsBrowserDistributedTracing",
    "AgentApplicationSettingsBrowserMonitoring",
    "AgentApplicationSettingsBrowserPrivacy",
    "AgentApplicationSettingsBrowserProperties",
    "AgentApplicationSettingsErrorCollector",
    "AgentApplicationSettingsIgnoredStatusCodeRule",
    "AgentApplicationSettingsJfr",
    "AgentApplicationSettingsMobileBase",
    "AgentApplicationSettingsMobileNetworkSettings",
    "AgentApplicationSettingsMobileProperties",
    "AgentApplicationSettingsNetworkAlias",
    "AgentApplicationSettingsSlowSql",
    "AgentApplicationSettingsThreadProfiler",
    "AgentApplicationSettingsTransactionTracer",
    "AgentApplicationSettingsUpdateError",
    "AgentApplicationSettingsUpdateResult",
    "AgentEnvironmentAccountApplicationLoadedModules",
    "AgentEnvironmentAccountApplicationLoadedModulesResults",
    "AgentEnvironmentAccountEnvironmentAttributesResults",
    "AgentEnvironmentAccountStitchedFields",
    "AgentEnvironmentApplicationEnvironmentAttributes",
    "AgentEnvironmentApplicationInstance",
    "AgentEnvironmentApplicationInstanceDetails",
    "AgentEnvironmentApplicationInstancesResult",
    "AgentEnvironmentApplicationLoadedModule",
    "AgentEnvironmentAttribute",
    "AgentEnvironmentLoadedModuleAttribute",
    "AgentFeatures",
    "AgentRelease",
    "AiDecisionsAccountStitchedFields",
    "AiDecisionsAnnotationEntry",
    "AiDecisionsApplicableIncidentSearch",
    "AiDecisionsDecision",
    "AiDecisionsDecisionListing",
    "AiDecisionsMergeFeedback",
    "AiDecisionsOperationResult",
    "AiDecisionsOpinionEntry",
    "AiDecisionsOverrideConfiguration",
    "AiDecisionsRule",
    "AiDecisionsRuleMetadata",
    "AiDecisionsSelectorApplicability",
    "AiDecisionsSelectorExamples",
    "AiDecisionsSimulation",
    "AiDecisionsSuggestion",
    "AiIssuesAccountStitchedFields",
    "AiIssuesConfigurationByEnvironment",
    "AiIssuesConfigurationOverrideResponse",
    "AiIssuesEnvironmentConfiguration",
    "AiIssuesGracePeriodConfig",
    "AiIssuesIncidentData",
    "AiIssuesIncidentUserActionResponse",
    "AiIssuesIssue",
    "AiIssuesIssueData",
    "AiIssuesIssueUserActionResponse",
    "AiIssuesIssueUserActionResult",
    "AiIssuesKeyValue",
    "AiIssuesKeyValues",
    "AiNotificationsAccountStitchedFields",
    "AiNotificationsBasicAuth",
    "AiNotificationsChannel",
    "AiNotificationsChannelResponse",
    "AiNotificationsChannelSchemaResult",
    "AiNotificationsChannelTestResponse",
    "AiNotificationsChannelsResponse",
    "AiNotificationsConstraintError",
    "AiNotificationsConstraintsError",
    "AiNotificationsDataValidationError",
    "AiNotificationsDeleteResponse",
    "AiNotificationsDestination",
    "AiNotificationsDestinationResponse",
    "AiNotificationsDestinationTestResponse",
    "AiNotificationsDestinationsResponse",
    "AiNotificationsFieldError",
    "AiNotificationsOAuth2Auth",
    "AiNotificationsOAuthUrlResponse",
    "AiNotificationsProperty",
    "AiNotificationsResponseError",
    "AiNotificationsSchema",
    "AiNotificationsSchemaField",
    "AiNotificationsSelectComponentOptions",
    "AiNotificationsSuggestion",
    "AiNotificationsSuggestionError",
    "AiNotificationsSuggestionsResponse",
    "AiNotificationsTokenAuth",
    "AiNotificationsUiComponent",
    "AiNotificationsVariable",
    "AiNotificationsVariableResult",
    "AiTopologyAccountStitchedFields",
    "AiTopologyCollectorOperationResult",
    "AiTopologyDefiningAttribute",
    "AiTopologyEdge",
    "AiTopologyEdgeListing",
    "AiTopologyGraph",
    "AiTopologyVertex",
    "AiTopologyVertexListing",
    "AiWorkflowsAccountStitchedFields",
    "AiWorkflowsCreateWorkflowResponse",
    "AiWorkflowsDeleteWorkflowResponse",
    "AiWorkflowsDestinationConfiguration",
    "AiWorkflowsEnrichment",
    "AiWorkflowsFilter",
    "AiWorkflowsNrqlConfiguration",
    "AiWorkflowsPredicate",
    "AiWorkflowsTestNotificationResponse",
    "AiWorkflowsTestWorkflowResponse",
    "AiWorkflowsUpdateWorkflowResponse",
    "AiWorkflowsWorkflow",
    "AiWorkflowsWorkflows",
    "AlertsAccountStitchedFields",
    "AlertsCampfireNotificationChannelConfig",
    "AlertsConditionDeleteResponse",
    "AlertsEmailNotificationChannelConfig",
    "AlertsHipChatNotificationChannelConfig",
    "AlertsMutingRule",
    "AlertsMutingRuleCondition",
    "AlertsMutingRuleConditionGroup",
    "AlertsMutingRuleDeleteResponse",
    "AlertsMutingRuleSchedule",
    "AlertsNotificationChannelCreateError",
    "AlertsNotificationChannelCreateResponse",
    "AlertsNotificationChannelDeleteError",
    "AlertsNotificationChannelDeleteResponse",
    "AlertsNotificationChannelId",
    "AlertsNotificationChannelPoliciesResultSet",
    "AlertsNotificationChannelPolicy",
    "AlertsNotificationChannelUpdateError",
    "AlertsNotificationChannelUpdateResponse",
    "AlertsNotificationChannelsAddToPolicyError",
    "AlertsNotificationChannelsAddToPolicyResponse",
    "AlertsNotificationChannelsRemoveFromPolicyError",
    "AlertsNotificationChannelsRemoveFromPolicyResponse",
    "AlertsNotificationChannelsResultSet",
    "AlertsNrqlConditionExpiration",
    "AlertsNrqlConditionQuery",
    "AlertsNrqlConditionSignal",
    "AlertsNrqlConditionTerms",
    "AlertsNrqlConditionsSearchResultSet",
    "AlertsOpsGenieNotificationChannelConfig",
    "AlertsPagerDutyNotificationChannelConfig",
    "AlertsPoliciesSearchResultSet",
    "AlertsPolicy",
    "AlertsPolicyDeleteResponse",
    "AlertsSlackNotificationChannelConfig",
    "AlertsUserNotificationChannelConfig",
    "AlertsVictorOpsNotificationChannelConfig",
    "AlertsWebhookBasicAuthInput",
    "AlertsWebhookCustomHeaderInput",
    "AlertsWebhookNotificationChannelConfig",
    "AlertsXMattersNotificationChannelConfig",
    "ApiAccessActorStitchedFields",
    "ApiAccessCreateKeyResponse",
    "ApiAccessDeleteKeyResponse",
    "ApiAccessDeletedKey",
    "ApiAccessKeySearchResult",
    "ApiAccessUpdateKeyResponse",
    "ApmApplicationDeployment",
    "ApmApplicationEntitySettingsResult",
    "ApmApplicationRunningAgentVersions",
    "ApmApplicationSettings",
    "ApmApplicationSummaryData",
    "ApmBrowserApplicationSummaryData",
    "ApmExternalServiceSummaryData",
    "AuthorizationManagementAuthenticationDomain",
    "AuthorizationManagementAuthenticationDomainSearch",
    "AuthorizationManagementGrantAccessPayload",
    "AuthorizationManagementGrantedRole",
    "AuthorizationManagementGrantedRoleSearch",
    "AuthorizationManagementGroup",
    "AuthorizationManagementGroupSearch",
    "AuthorizationManagementOrganizationStitchedFields",
    "AuthorizationManagementRevokeAccessPayload",
    "AuthorizationManagementRole",
    "AuthorizationManagementRoleSearch",
    "BrowserApplicationRunningAgentVersions",
    "BrowserApplicationSettings",
    "BrowserApplicationSummaryData",
    "ChangeTrackingDeployment",
    "ChangeTrackingDeploymentSearchResult",
    "CloudAccountFields",
    "CloudAccountMutationError",
    "CloudActorFields",
    "CloudConfigureIntegrationPayload",
    "CloudDisableIntegrationPayload",
    "CloudIntegrationMutationError",
    "CloudLinkAccountPayload",
    "CloudLinkedAccount",
    "CloudMigrateAwsGovCloudToAssumeRolePayload",
    "CloudRenameAccountPayload",
    "CloudService",
    "CloudUnlinkAccountPayload",
    "CrossAccountNrdbResultContainer",
    "DashboardActorStitchedFields",
    "DashboardAddWidgetsToPageError",
    "DashboardAddWidgetsToPageResult",
    "DashboardAreaWidgetConfiguration",
    "DashboardBarWidgetConfiguration",
    "DashboardBillboardWidgetConfiguration",
    "DashboardBillboardWidgetThreshold",
    "DashboardCreateError",
    "DashboardCreateResult",
    "DashboardDeleteError",
    "DashboardDeleteResult",
    "DashboardEntityOwnerInfo",
    "DashboardEntityResult",
    "DashboardLineWidgetConfiguration",
    "DashboardLiveUrl",
    "DashboardLiveUrlError",
    "DashboardLiveUrlResult",
    "DashboardMarkdownWidgetConfiguration",
    "DashboardOwnerInfo",
    "DashboardPage",
    "DashboardPieWidgetConfiguration",
    "DashboardRevokeLiveUrlResult",
    "DashboardTableWidgetConfiguration",
    "DashboardUndeleteError",
    "DashboardUndeleteResult",
    "DashboardUpdateError",
    "DashboardUpdatePageError",
    "DashboardUpdatePageResult",
    "DashboardUpdateResult",
    "DashboardUpdateWidgetsInPageError",
    "DashboardUpdateWidgetsInPageResult",
    "DashboardVariable",
    "DashboardVariableDefaultItem",
    "DashboardVariableDefaultValue",
    "DashboardVariableEnumItem",
    "DashboardVariableNrqlQuery",
    "DashboardWidget",
    "DashboardWidgetConfiguration",
    "DashboardWidgetLayout",
    "DashboardWidgetNrqlQuery",
    "DashboardWidgetVisualization",
    "DataDictionaryAttribute",
    "DataDictionaryDataSource",
    "DataDictionaryDocsStitchedFields",
    "DataDictionaryEvent",
    "DataDictionaryUnit",
    "DataManagementAccountLimit",
    "DataManagementAccountStitchedFields",
    "DataManagementAppliedRules",
    "DataManagementBulkCopyResult",
    "DataManagementCustomizableRetention",
    "DataManagementEventNamespaces",
    "DataManagementFeatureSetting",
    "DataManagementNamespaceLevelRetention",
    "DataManagementRenderedRetention",
    "DataManagementRetention",
    "DataManagementRetentionValues",
    "DataManagementRule",
    "DateTimeWindow",
    "DistributedTracingActorStitchedFields",
    "DistributedTracingEntityTracingSummary",
    "DistributedTracingSpan",
    "DistributedTracingSpanAnomaly",
    "DistributedTracingSpanConnection",
    "DistributedTracingTrace",
    "DocumentationFields",
    "DomainType",
    "EdgeAccountStitchedFields",
    "EdgeCreateSpanAttributeRuleResponseError",
    "EdgeCreateSpanAttributeRulesResponse",
    "EdgeCreateTraceFilterRuleResponses",
    "EdgeCreateTraceObserverResponse",
    "EdgeCreateTraceObserverResponseError",
    "EdgeCreateTraceObserverResponses",
    "EdgeDataSource",
    "EdgeDataSourceGroup",
    "EdgeDeleteSpanAttributeRuleResponse",
    "EdgeDeleteSpanAttributeRuleResponseError",
    "EdgeDeleteTraceFilterRuleResponses",
    "EdgeDeleteTraceObserverResponse",
    "EdgeDeleteTraceObserverResponseError",
    "EdgeDeleteTraceObserverResponses",
    "EdgeEndpoint",
    "EdgeRandomTraceFilter",
    "EdgeSpanAttributeRule",
    "EdgeSpanAttributesTraceFilter",
    "EdgeTraceFilters",
    "EdgeTraceObserver",
    "EdgeTracing",
    "EdgeUpdateTraceObserverResponse",
    "EdgeUpdateTraceObserverResponseError",
    "EdgeUpdateTraceObserverResponses",
    "EntityAlertViolation",
    "EntityCollection",
    "EntityCollectionDefinition",
    "EntityCollectionScopeAccounts",
    "EntityDeleteError",
    "EntityDeleteResult",
    "EntityGoldenContext",
    "EntityGoldenContextScopedGoldenMetrics",
    "EntityGoldenContextScopedGoldenTags",
    "EntityGoldenGoldenMetricsError",
    "EntityGoldenMetric",
    "EntityGoldenMetricDefinition",
    "EntityGoldenMetricsDomainTypeScoped",
    "EntityGoldenMetricsDomainTypeScopedResponse",
    "EntityGoldenOriginalDefinitionWithSelector",
    "EntityGoldenOriginalQueryWithSelector",
    "EntityGoldenTag",
    "EntityGoldenTagsDomainTypeScoped",
    "EntityGoldenTagsDomainTypeScopedResponse",
    "EntityRelationship",
    "EntityRelationshipNode",
    "EntityRelationshipRelatedEntitiesResult",
    "EntityRelationshipUserDefinedCreateOrReplaceResult",
    "EntityRelationshipUserDefinedCreateOrReplaceResultError",
    "EntityRelationshipUserDefinedDeleteResult",
    "EntityRelationshipUserDefinedDeleteResultError",
    "EntityRelationshipVertex",
    "EntitySearch",
    "EntitySearchCounts",
    "EntitySearchResult",
    "EntitySearchTypes",
    "EntityTag",
    "EntityTagValueWithMetadata",
    "EntityTagWithMetadata",
    "ErrorsInboxActorStitchedFields",
    "ErrorsInboxAssignErrorGroupResponse",
    "ErrorsInboxAssignment",
    "ErrorsInboxDeleteErrorGroupResourceResponse",
    "ErrorsInboxErrorGroup",
    "ErrorsInboxErrorGroupStateTypeResult",
    "ErrorsInboxErrorGroupsResponse",
    "ErrorsInboxOccurrences",
    "ErrorsInboxResourcesResponse",
    "ErrorsInboxUpdateErrorGroupStateResponse",
    "EventAttributeDefinition",
    "EventDefinition",
    "EventsToMetricsAccountStitchedFields",
    "EventsToMetricsCreateRuleFailure",
    "EventsToMetricsCreateRuleResult",
    "EventsToMetricsCreateRuleSubmission",
    "EventsToMetricsDeleteRuleFailure",
    "EventsToMetricsDeleteRuleResult",
    "EventsToMetricsDeleteRuleSubmission",
    "EventsToMetricsError",
    "EventsToMetricsListRuleResult",
    "EventsToMetricsRule",
    "EventsToMetricsUpdateRuleFailure",
    "EventsToMetricsUpdateRuleResult",
    "EventsToMetricsUpdateRuleSubmission",
    "HistoricalDataExportAccountStitchedFields",
    "HistoricalDataExportCustomerExportResponse",
    "IncidentIntelligenceEnvironmentAccountStitchedFields",
    "IncidentIntelligenceEnvironmentActorStitchedFields",
    "IncidentIntelligenceEnvironmentConsentAccounts",
    "IncidentIntelligenceEnvironmentConsentAuthorizedAccounts",
    "IncidentIntelligenceEnvironmentConsentedAccount",
    "IncidentIntelligenceEnvironmentCreateEnvironment",
    "IncidentIntelligenceEnvironmentCurrentEnvironmentResult",
    "IncidentIntelligenceEnvironmentDeleteEnvironment",
    "IncidentIntelligenceEnvironmentDissentAccounts",
    "IncidentIntelligenceEnvironmentEnvironmentAlreadyExists",
    "IncidentIntelligenceEnvironmentEnvironmentCreated",
    "IncidentIntelligenceEnvironmentIncidentIntelligenceEnvironment",
    "IncidentIntelligenceEnvironmentMultipleEnvironmentsAvailable",
    "IncidentIntelligenceEnvironmentUserNotAuthorizedForAccount",
    "IncidentIntelligenceEnvironmentUserNotCapableToOperateOnAccount",
    "InfrastructureHostSummaryData",
    "InstallationAccountStitchedFields",
    "InstallationInstallStatus",
    "InstallationInstallStatusResult",
    "InstallationRecipeEvent",
    "InstallationRecipeEventResult",
    "InstallationStatusError",
    "JavaFlightRecorderFlamegraph",
    "JavaFlightRecorderStackFrame",
    "KeyTransactionApplication",
    "KeyTransactionCreateResult",
    "KeyTransactionDeleteResult",
    "KeyTransactionUpdateResult",
    "LogConfigurationsAccountStitchedFields",
    "LogConfigurationsCreateDataPartitionRuleError",
    "LogConfigurationsCreateDataPartitionRuleResponse",
    "LogConfigurationsCreateParsingRuleResponse",
    "LogConfigurationsDataPartitionRule",
    "LogConfigurationsDataPartitionRuleMatchingCriteria",
    "LogConfigurationsDataPartitionRuleMutationError",
    "LogConfigurationsDeleteDataPartitionRuleResponse",
    "LogConfigurationsDeleteParsingRuleResponse",
    "LogConfigurationsGrokTestExtractedAttribute",
    "LogConfigurationsGrokTestResult",
    "LogConfigurationsObfuscationAction",
    "LogConfigurationsObfuscationExpression",
    "LogConfigurationsObfuscationRule",
    "LogConfigurationsParsingRule",
    "LogConfigurationsParsingRuleMutationError",
    "LogConfigurationsPipelineConfiguration",
    "LogConfigurationsUpdateDataPartitionRuleResponse",
    "LogConfigurationsUpdateParsingRuleResponse",
    "LogConfigurationsUpsertPipelineConfigurationResponse",
    "MetricNormalizationAccountStitchedFields",
    "MetricNormalizationRule",
    "MetricNormalizationRuleMetricGroupingIssue",
    "MetricNormalizationRuleMutationError",
    "MetricNormalizationRuleMutationResponse",
    "MobileAppSummaryData",
    "MobilePushNotificationActorStitchedFields",
    "MobilePushNotificationDevice",
    "MobilePushNotificationRemoveDeviceResult",
    "MobilePushNotificationSendPushResult",
    "NerdStorageAccountScope",
    "NerdStorageActorScope",
    "NerdStorageCollectionMember",
    "NerdStorageDeleteResult",
    "NerdStorageEntityScope",
    "NerdStorageVaultActorStitchedFields",
    "NerdStorageVaultDeleteSecretResult",
    "NerdStorageVaultResultError",
    "NerdStorageVaultSecret",
    "NerdStorageVaultWriteSecretResult",
    "NerdpackAllowListResult",
    "NerdpackAllowedAccount",
    "NerdpackAssetInfo",
    "NerdpackData",
    "NerdpackMutationResultPerAccount",
    "NerdpackNerdpacks",
    "NerdpackRemovedTagInfo",
    "NerdpackRemovedTagResponse",
    "NerdpackSubscribeResult",
    "NerdpackSubscription",
    "NerdpackUnsubscribeResult",
    "NerdpackVersion",
    "NerdpackVersionsResult",
    "Nr1CatalogActorStitchedFields",
    "Nr1CatalogAlertConditionOutline",
    "Nr1CatalogAlertConditionTemplate",
    "Nr1CatalogAlertConditionTemplateMetadata",
    "Nr1CatalogAlertPolicyOutline",
    "Nr1CatalogAlertPolicyTemplate",
    "Nr1CatalogAlertPolicyTemplateMetadata",
    "Nr1CatalogAuthor",
    "Nr1CatalogCategory",
    "Nr1CatalogCategoryFacet",
    "Nr1CatalogCommunityContactChannel",
    "Nr1CatalogComponentFacet",
    "Nr1CatalogDashboardOutline",
    "Nr1CatalogDashboardTemplate",
    "Nr1CatalogDashboardTemplateMetadata",
    "Nr1CatalogDataSource",
    "Nr1CatalogDataSourceInstall",
    "Nr1CatalogDataSourceMetadata",
    "Nr1CatalogEmailContactChannel",
    "Nr1CatalogIcon",
    "Nr1CatalogInstallAlertPolicyTemplateResult",
    "Nr1CatalogInstallDashboardTemplateResult",
    "Nr1CatalogInstallPlanStep",
    "Nr1CatalogInstallPlanTarget",
    "Nr1CatalogIssuesContactChannel",
    "Nr1CatalogLinkInstallDirective",
    "Nr1CatalogNerdletInstallDirective",
    "Nr1CatalogNerdpack",
    "Nr1CatalogNerdpackMetadata",
    "Nr1CatalogQuickstart",
    "Nr1CatalogQuickstartMetadata",
    "Nr1CatalogQuickstartsListing",
    "Nr1CatalogReleaseNote",
    "Nr1CatalogSearchFacets",
    "Nr1CatalogSearchResponse",
    "Nr1CatalogSearchResultTypeFacet",
    "Nr1CatalogSubmitMetadataError",
    "Nr1CatalogSubmitMetadataResult",
    "Nr1CatalogSupportChannels",
    "NrdbMetadata",
    "NrdbMetadataTimeWindow",
    "NrdbQueryProgress",
    "NrdbResultContainer",
    "NrqlDropRulesAccountStitchedFields",
    "NrqlDropRulesCreateDropRuleFailure",
    "NrqlDropRulesCreateDropRuleResult",
    "NrqlDropRulesCreateDropRuleSubmission",
    "NrqlDropRulesDeleteDropRuleFailure",
    "NrqlDropRulesDeleteDropRuleResult",
    "NrqlDropRulesDeleteDropRuleSubmission",
    "NrqlDropRulesDropRule",
    "NrqlDropRulesError",
    "NrqlDropRulesListDropRulesResult",
    "NrqlFacetSuggestion",
    "NrqlHistoricalQuery",
    "Organization",
    "OrganizationAccountShares",
    "OrganizationAuthenticationDomain",
    "OrganizationAuthenticationDomainCollection",
    "OrganizationCreateSharedAccountResponse",
    "OrganizationCustomerOrganization",
    "OrganizationCustomerOrganizationWrapper",
    "OrganizationError",
    "OrganizationInformation",
    "OrganizationOrganizationAdministrator",
    "OrganizationProvisioningUpdateSubscriptionResult",
    "OrganizationProvisioningUserError",
    "OrganizationRevokeSharedAccountResponse",
    "OrganizationSharedAccount",
    "OrganizationUpdateResponse",
    "OrganizationUpdateSharedAccountResponse",
    "PixieAccountStitchedFields",
    "PixieActorStitchedFields",
    "PixieLinkPixieProjectError",
    "PixieLinkPixieProjectResult",
    "PixieLinkedPixieProject",
    "PixiePixieProject",
    "PixieRecordPixieTosAcceptanceError",
    "PixieRecordPixieTosAcceptanceResult",
    "QueryHistoryActorStitchedFields",
    "QueryHistoryNrqlHistoryResult",
    "ReferenceEntityCreateRepositoryError",
    "ReferenceEntityCreateRepositoryResult",
    "RequestContext",
    "RootMutationType",
    "RootQueryType",
    "SecureCredentialSummaryData",
    "ServiceLevelDefinition",
    "ServiceLevelEvents",
    "ServiceLevelEventsQuery",
    "ServiceLevelEventsQuerySelect",
    "ServiceLevelIndicator",
    "ServiceLevelIndicatorResultQueries",
    "ServiceLevelObjective",
    "ServiceLevelObjectiveResultQueries",
    "ServiceLevelObjectiveRollingTimeWindow",
    "ServiceLevelObjectiveTimeWindow",
    "ServiceLevelResultQuery",
    "StackTraceApmException",
    "StackTraceApmStackTrace",
    "StackTraceApmStackTraceFrame",
    "StackTraceBrowserException",
    "StackTraceBrowserStackTrace",
    "StackTraceBrowserStackTraceFrame",
    "StackTraceMobileCrash",
    "StackTraceMobileCrashStackTrace",
    "StackTraceMobileCrashStackTraceFrame",
    "StackTraceMobileException",
    "StackTraceMobileExceptionStackTrace",
    "StackTraceMobileExceptionStackTraceFrame",
    "StreamingExportAccountStitchedFields",
    "StreamingExportAwsDetails",
    "StreamingExportAzureDetails",
    "StreamingExportRule",
    "SuggestedNrqlQueryAnomaly",
    "SuggestedNrqlQueryResponse",
    "SyntheticMonitorSummaryData",
    "SyntheticsAccountStitchedFields",
    "SyntheticsBrokenLinksMonitor",
    "SyntheticsBrokenLinksMonitorCreateMutationResult",
    "SyntheticsBrokenLinksMonitorUpdateMutationResult",
    "SyntheticsCertCheckMonitor",
    "SyntheticsCertCheckMonitorCreateMutationResult",
    "SyntheticsCertCheckMonitorUpdateMutationResult",
    "SyntheticsCustomHeader",
    "SyntheticsDeviceEmulation",
    "SyntheticsError",
    "SyntheticsLocations",
    "SyntheticsMonitorCreateError",
    "SyntheticsMonitorDeleteMutationResult",
    "SyntheticsMonitorScriptQueryResponse",
    "SyntheticsMonitorUpdateError",
    "SyntheticsPrivateLocationDeleteResult",
    "SyntheticsPrivateLocationMutationError",
    "SyntheticsPrivateLocationMutationResult",
    "SyntheticsPrivateLocationPurgeQueueResult",
    "SyntheticsRuntime",
    "SyntheticsScriptApiMonitor",
    "SyntheticsScriptApiMonitorCreateMutationResult",
    "SyntheticsScriptApiMonitorUpdateMutationResult",
    "SyntheticsScriptBrowserMonitor",
    "SyntheticsScriptBrowserMonitorAdvancedOptions",
    "SyntheticsScriptBrowserMonitorCreateMutationResult",
    "SyntheticsScriptBrowserMonitorUpdateMutationResult",
    "SyntheticsSecureCredentialMutationResult",
    "SyntheticsSimpleBrowserMonitor",
    "SyntheticsSimpleBrowserMonitorAdvancedOptions",
    "SyntheticsSimpleBrowserMonitorCreateMutationResult",
    "SyntheticsSimpleBrowserMonitorUpdateMutationResult",
    "SyntheticsSimpleMonitor",
    "SyntheticsSimpleMonitorAdvancedOptions",
    "SyntheticsSimpleMonitorUpdateMutationResult",
    "SyntheticsStep",
    "SyntheticsStepMonitor",
    "SyntheticsStepMonitorAdvancedOptions",
    "SyntheticsStepMonitorCreateMutationResult",
    "SyntheticsStepMonitorUpdateMutationResult",
    "SyntheticsSyntheticMonitorAsset",
    "TaggingMutationError",
    "TaggingMutationResult",
    "TimeWindow",
    "TimeZoneInfo",
    "User",
    "UserManagementAddUsersToGroupsPayload",
    "UserManagementAuthenticationDomain",
    "UserManagementAuthenticationDomains",
    "UserManagementCreateGroupPayload",
    "UserManagementCreateUserPayload",
    "UserManagementCreatedUser",
    "UserManagementDeleteGroupPayload",
    "UserManagementDeleteUserPayload",
    "UserManagementDeletedUser",
    "UserManagementGroup",
    "UserManagementGroupUser",
    "UserManagementGroupUsers",
    "UserManagementGroups",
    "UserManagementOrganizationStitchedFields",
    "UserManagementOrganizationUserType",
    "UserManagementPendingUpgradeRequest",
    "UserManagementRemoveUsersFromGroupsPayload",
    "UserManagementUpdateGroupPayload",
    "UserManagementUpdateUserPayload",
    "UserManagementUser",
    "UserManagementUserGroup",
    "UserManagementUserGroups",
    "UserManagementUserType",
    "UserManagementUsers",
    "UserReference",
    "UsersActorStitchedFields",
    "UsersUserSearch",
    "UsersUserSearchResult",
    "WhatsNewDocsStitchedFields",
    "WhatsNewSearchResult",
    "WorkloadAccountStitchedFields",
    "WorkloadAutomaticStatus",
    "WorkloadCollection",
    "WorkloadCollectionWithoutStatus",
    "WorkloadEntityRef",
    "WorkloadEntitySearchQuery",
    "WorkloadRegularRule",
    "WorkloadRemainingEntitiesRule",
    "WorkloadRemainingEntitiesRuleRollup",
    "WorkloadRollup",
    "WorkloadRollupRuleDetails",
    "WorkloadScopeAccounts",
    "WorkloadStaticStatus",
    "WorkloadStatus",
    "WorkloadStatusConfig",
    "WorkloadValidAccounts",
    "WorkloadWorkloadStatus",
    "AiIssuesAnomalyIncident",
    "AiIssuesNewRelicIncident",
    "AiIssuesRestIncident",
    "AiWorkflowsCreateResponseError",
    "AiWorkflowsDeleteResponseError",
    "AiWorkflowsTestResponseError",
    "AiWorkflowsUpdateResponseError",
    "AlertsCampfireNotificationChannel",
    "AlertsEmailNotificationChannel",
    "AlertsHipChatNotificationChannel",
    "AlertsNrqlBaselineCondition",
    "AlertsNrqlOutlierCondition",
    "AlertsNrqlStaticCondition",
    "AlertsOpsGenieNotificationChannel",
    "AlertsPagerDutyNotificationChannel",
    "AlertsSlackNotificationChannel",
    "AlertsUserNotificationChannel",
    "AlertsVictorOpsNotificationChannel",
    "AlertsWebhookNotificationChannel",
    "AlertsXMattersNotificationChannel",
    "ApiAccessIngestKey",
    "ApiAccessIngestKeyError",
    "ApiAccessUserKey",
    "ApiAccessUserKeyError",
    "ApmApplicationEntity",
    "ApmApplicationEntityOutline",
    "ApmDatabaseInstanceEntity",
    "ApmDatabaseInstanceEntityOutline",
    "ApmExternalServiceEntity",
    "ApmExternalServiceEntityOutline",
    "BrowserApplicationEntity",
    "BrowserApplicationEntityOutline",
    "CloudAlbIntegration",
    "CloudApigatewayIntegration",
    "CloudAutoscalingIntegration",
    "CloudAwsAppsyncIntegration",
    "CloudAwsAthenaIntegration",
    "CloudAwsCognitoIntegration",
    "CloudAwsConnectIntegration",
    "CloudAwsDirectconnectIntegration",
    "CloudAwsDocdbIntegration",
    "CloudAwsFsxIntegration",
    "CloudAwsGlueIntegration",
    "CloudAwsGovCloudProvider",
    "CloudAwsKinesisanalyticsIntegration",
    "CloudAwsMediaconvertIntegration",
    "CloudAwsMediapackagevodIntegration",
    "CloudAwsMetadataIntegration",
    "CloudAwsMqIntegration",
    "CloudAwsMskIntegration",
    "CloudAwsNeptuneIntegration",
    "CloudAwsProvider",
    "CloudAwsQldbIntegration",
    "CloudAwsRoute53resolverIntegration",
    "CloudAwsStatesIntegration",
    "CloudAwsTagsGlobalIntegration",
    "CloudAwsTransitgatewayIntegration",
    "CloudAwsWafIntegration",
    "CloudAwsWafv2Integration",
    "CloudAwsXrayIntegration",
    "CloudAzureApimanagementIntegration",
    "CloudAzureAppgatewayIntegration",
    "CloudAzureAppserviceIntegration",
    "CloudAzureContainersIntegration",
    "CloudAzureCosmosdbIntegration",
    "CloudAzureCostmanagementIntegration",
    "CloudAzureDatafactoryIntegration",
    "CloudAzureEventhubIntegration",
    "CloudAzureExpressrouteIntegration",
    "CloudAzureFirewallsIntegration",
    "CloudAzureFrontdoorIntegration",
    "CloudAzureFunctionsIntegration",
    "CloudAzureKeyvaultIntegration",
    "CloudAzureLoadbalancerIntegration",
    "CloudAzureLogicappsIntegration",
    "CloudAzureMachinelearningIntegration",
    "CloudAzureMariadbIntegration",
    "CloudAzureMonitorIntegration",
    "CloudAzureMysqlIntegration",
    "CloudAzureMysqlflexibleIntegration",
    "CloudAzurePostgresqlIntegration",
    "CloudAzurePostgresqlflexibleIntegration",
    "CloudAzurePowerbidedicatedIntegration",
    "CloudAzureRediscacheIntegration",
    "CloudAzureServicebusIntegration",
    "CloudAzureSqlIntegration",
    "CloudAzureSqlmanagedIntegration",
    "CloudAzureStorageIntegration",
    "CloudAzureVirtualmachineIntegration",
    "CloudAzureVirtualnetworksIntegration",
    "CloudAzureVmsIntegration",
    "CloudAzureVpngatewaysIntegration",
    "CloudBaseIntegration",
    "CloudBaseProvider",
    "CloudBillingIntegration",
    "CloudCloudfrontIntegration",
    "CloudCloudtrailIntegration",
    "CloudDynamodbIntegration",
    "CloudEbsIntegration",
    "CloudEc2Integration",
    "CloudEcsIntegration",
    "CloudEfsIntegration",
    "CloudElasticacheIntegration",
    "CloudElasticbeanstalkIntegration",
    "CloudElasticsearchIntegration",
    "CloudElbIntegration",
    "CloudEmrIntegration",
    "CloudGcpAlloydbIntegration",
    "CloudGcpAppengineIntegration",
    "CloudGcpBigqueryIntegration",
    "CloudGcpBigtableIntegration",
    "CloudGcpComposerIntegration",
    "CloudGcpDataflowIntegration",
    "CloudGcpDataprocIntegration",
    "CloudGcpDatastoreIntegration",
    "CloudGcpFirebasedatabaseIntegration",
    "CloudGcpFirebasehostingIntegration",
    "CloudGcpFirebasestorageIntegration",
    "CloudGcpFirestoreIntegration",
    "CloudGcpFunctionsIntegration",
    "CloudGcpInterconnectIntegration",
    "CloudGcpKubernetesIntegration",
    "CloudGcpLoadbalancingIntegration",
    "CloudGcpMemcacheIntegration",
    "CloudGcpProvider",
    "CloudGcpPubsubIntegration",
    "CloudGcpRedisIntegration",
    "CloudGcpRouterIntegration",
    "CloudGcpRunIntegration",
    "CloudGcpSpannerIntegration",
    "CloudGcpSqlIntegration",
    "CloudGcpStorageIntegration",
    "CloudGcpVmsIntegration",
    "CloudGcpVpcaccessIntegration",
    "CloudHealthIntegration",
    "CloudIamIntegration",
    "CloudIotIntegration",
    "CloudKinesisFirehoseIntegration",
    "CloudKinesisIntegration",
    "CloudLambdaIntegration",
    "CloudRdsIntegration",
    "CloudRedshiftIntegration",
    "CloudRoute53Integration",
    "CloudS3Integration",
    "CloudSesIntegration",
    "CloudSnsIntegration",
    "CloudSqsIntegration",
    "CloudTrustedadvisorIntegration",
    "CloudVpcIntegration",
    "DashboardEntity",
    "DashboardEntityOutline",
    "EdgeAgentEndpointDetail",
    "EdgeHttpsEndpointDetail",
    "EntityRelationshipDetectedEdge",
    "EntityRelationshipUserDefinedEdge",
    "ErrorsInboxAssignErrorGroupError",
    "ErrorsInboxJiraIssue",
    "ErrorsInboxUpdateErrorGroupStateError",
    "ExternalEntity",
    "ExternalEntityOutline",
    "GenericEntity",
    "GenericEntityOutline",
    "GenericInfrastructureEntity",
    "GenericInfrastructureEntityOutline",
    "InfrastructureAwsLambdaFunctionEntity",
    "InfrastructureAwsLambdaFunctionEntityOutline",
    "InfrastructureHostEntity",
    "InfrastructureHostEntityOutline",
    "KeyTransactionEntity",
    "KeyTransactionEntityOutline",
    "MobileApplicationEntity",
    "MobileApplicationEntityOutline",
    "Nr1CatalogAllSupportedEntityTypes",
    "Nr1CatalogInstallPlan",
    "Nr1CatalogLauncher",
    "Nr1CatalogLauncherMetadata",
    "Nr1CatalogLinkInstallPlanDirective",
    "Nr1CatalogNerdlet",
    "Nr1CatalogNerdletInstallPlanDirective",
    "Nr1CatalogNerdletMetadata",
    "Nr1CatalogNoSupportedEntityTypes",
    "Nr1CatalogQuickstartAlert",
    "Nr1CatalogQuickstartAlertCondition",
    "Nr1CatalogQuickstartAlertConditionMetadata",
    "Nr1CatalogQuickstartAlertMetadata",
    "Nr1CatalogQuickstartDashboard",
    "Nr1CatalogQuickstartDashboardMetadata",
    "Nr1CatalogQuickstartDocumentation",
    "Nr1CatalogQuickstartDocumentationMetadata",
    "Nr1CatalogQuickstartInstallPlan",
    "Nr1CatalogQuickstartInstallPlanMetadata",
    "Nr1CatalogScreenshot",
    "Nr1CatalogSpecificSupportedEntityTypes",
    "Nr1CatalogTargetedInstallPlanDirective",
    "Nr1CatalogVisualization",
    "Nr1CatalogVisualizationMetadata",
    "SecureCredentialEntity",
    "SecureCredentialEntityOutline",
    "SuggestedAnomalyBasedNrqlQuery",
    "SuggestedHistoryBasedNrqlQuery",
    "SyntheticMonitorEntity",
    "SyntheticMonitorEntityOutline",
    "TeamEntity",
    "TeamEntityOutline",
    "ThirdPartyServiceEntity",
    "ThirdPartyServiceEntityOutline",
    "UnavailableEntity",
    "UnavailableEntityOutline",
    "WhatsNewAnnouncementContent",
    "WorkloadEntity",
    "WorkloadEntityOutline",
    "WorkloadRollupRuleStatusResult",
    "WorkloadStaticStatusResult",
    "AiNotificationsAuth",
    "AiNotificationsError",
    "AiWorkflowsConfiguration",
    "AlertsNotificationChannelMutation",
    "IncidentIntelligenceEnvironmentCreateEnvironmentResultDetails",
    "IncidentIntelligenceEnvironmentCurrentEnvironmentResultReasonDetails",
    "Nr1CatalogDataSourceInstallDirective",
    "Nr1CatalogSearchResult",
]


# pylint: disable=duplicate-code,unused-import,too-many-lines,disallowed-name


import sgqlc.types
import sgqlc.types.datetime

from newrelic_sb_sdk.graphql.enums import (
    AgentApplicationBrowserLoader,
    AgentApplicationSettingsBrowserLoader,
    AgentApplicationSettingsNetworkFilterMode,
    AgentApplicationSettingsRecordSqlEnum,
    AgentApplicationSettingsThresholdTypeEnum,
    AgentApplicationSettingsTracer,
    AgentApplicationSettingsUpdateErrorClass,
    AgentFeaturesFilter,
    AgentReleasesFilter,
    AiDecisionsDecisionSortMethod,
    AiDecisionsDecisionState,
    AiDecisionsDecisionType,
    AiDecisionsIncidentSelect,
    AiDecisionsIssuePriority,
    AiDecisionsOpinion,
    AiDecisionsResultType,
    AiDecisionsRuleSource,
    AiDecisionsRuleState,
    AiDecisionsRuleType,
    AiDecisionsSuggestionState,
    AiIssuesIncidentState,
    AiIssuesIssueMutingState,
    AiIssuesIssueState,
    AiIssuesIssueUserAction,
    AiIssuesPriority,
    AiNotificationsAuthType,
    AiNotificationsChannelStatus,
    AiNotificationsChannelType,
    AiNotificationsDestinationStatus,
    AiNotificationsDestinationType,
    AiNotificationsErrorType,
    AiNotificationsProduct,
    AiNotificationsResult,
    AiNotificationsUiComponentType,
    AiNotificationsUiComponentValidation,
    AiNotificationsVariableCategory,
    AiNotificationsVariableType,
    AiTopologyCollectorResultType,
    AiTopologyVertexClass,
    AiWorkflowsCreateErrorType,
    AiWorkflowsDeleteErrorType,
    AiWorkflowsDestinationType,
    AiWorkflowsEnrichmentType,
    AiWorkflowsFilterType,
    AiWorkflowsMutingRulesHandling,
    AiWorkflowsNotificationTrigger,
    AiWorkflowsOperator,
    AiWorkflowsTestErrorType,
    AiWorkflowsTestNotificationResponseStatus,
    AiWorkflowsTestResponseStatus,
    AiWorkflowsUpdateErrorType,
    AlertsDayOfWeek,
    AlertsFillOption,
    AlertsIncidentPreference,
    AlertsMutingRuleConditionGroupOperator,
    AlertsMutingRuleConditionOperator,
    AlertsMutingRuleScheduleRepeat,
    AlertsMutingRuleStatus,
    AlertsNotificationChannelCreateErrorType,
    AlertsNotificationChannelDeleteErrorType,
    AlertsNotificationChannelsAddToPolicyErrorType,
    AlertsNotificationChannelsRemoveFromPolicyErrorType,
    AlertsNotificationChannelType,
    AlertsNotificationChannelUpdateErrorType,
    AlertsNrqlBaselineDirection,
    AlertsNrqlConditionPriority,
    AlertsNrqlConditionTermsOperator,
    AlertsNrqlConditionThresholdOccurrences,
    AlertsNrqlConditionType,
    AlertsOpsGenieDataCenterRegion,
    AlertsSignalAggregationMethod,
    AlertsWebhookCustomPayloadType,
    ApiAccessIngestKeyErrorType,
    ApiAccessIngestKeyType,
    ApiAccessKeyType,
    ApiAccessUserKeyErrorType,
    BrowserAgentInstallType,
    ChangeTrackingDeploymentType,
    ChartFormatType,
    ChartImageType,
    CloudMetricCollectionMode,
    DashboardAddWidgetsToPageErrorType,
    DashboardAlertSeverity,
    DashboardCreateErrorType,
    DashboardDeleteErrorType,
    DashboardDeleteResultStatus,
    DashboardEntityPermissions,
    DashboardLiveUrlErrorType,
    DashboardLiveUrlType,
    DashboardPermissions,
    DashboardUndeleteErrorType,
    DashboardUpdateErrorType,
    DashboardUpdatePageErrorType,
    DashboardUpdateWidgetsInPageErrorType,
    DashboardVariableReplacementStrategy,
    DashboardVariableType,
    DataDictionaryTextFormat,
    DataManagementCategory,
    DataManagementUnit,
    DistributedTracingSpanAnomalyType,
    DistributedTracingSpanClientType,
    DistributedTracingSpanProcessBoundary,
    EdgeComplianceTypeCode,
    EdgeCreateSpanAttributeRuleResponseErrorType,
    EdgeCreateTraceObserverResponseErrorType,
    EdgeDataSourceStatusType,
    EdgeDeleteSpanAttributeRuleResponseErrorType,
    EdgeDeleteTraceObserverResponseErrorType,
    EdgeEndpointStatus,
    EdgeEndpointType,
    EdgeProviderRegion,
    EdgeSpanAttributeKeyOperator,
    EdgeSpanAttributeValueOperator,
    EdgeTraceFilterAction,
    EdgeTraceObserverStatus,
    EdgeUpdateTraceObserverResponseErrorType,
    EmbeddedChartType,
    EntityAlertSeverity,
    EntityCollectionType,
    EntityDeleteErrorType,
    EntityGoldenEventObjectId,
    EntityGoldenGoldenMetricsErrorType,
    EntityGoldenMetricUnit,
    EntityRelationshipEdgeType,
    EntityRelationshipType,
    EntityRelationshipUserDefinedCreateOrReplaceErrorType,
    EntityRelationshipUserDefinedDeleteErrorType,
    EntitySearchCountsFacet,
    EntitySearchSortCriteria,
    EntityType,
    ErrorsInboxAssignErrorGroupErrorType,
    ErrorsInboxErrorGroupState,
    ErrorsInboxUpdateErrorGroupStateErrorType,
    EventsToMetricsErrorReason,
    HistoricalDataExportStatus,
    IncidentIntelligenceEnvironmentConsentAccountsResult,
    IncidentIntelligenceEnvironmentCreateEnvironmentResult,
    IncidentIntelligenceEnvironmentCurrentEnvironmentResultReason,
    IncidentIntelligenceEnvironmentDeleteEnvironmentResult,
    IncidentIntelligenceEnvironmentDissentAccountsResult,
    IncidentIntelligenceEnvironmentEnvironmentKind,
    IncidentIntelligenceEnvironmentSupportedEnvironmentKind,
    InstallationInstallStateType,
    InstallationRecipeStatusType,
    LogConfigurationsCreateDataPartitionRuleErrorType,
    LogConfigurationsDataPartitionRuleMatchingOperator,
    LogConfigurationsDataPartitionRuleMutationErrorType,
    LogConfigurationsDataPartitionRuleRetentionPolicyType,
    LogConfigurationsObfuscationMethod,
    LogConfigurationsParsingRuleMutationErrorType,
    MetricNormalizationRuleAction,
    MetricNormalizationRuleErrorType,
    NerdpackMutationErrorType,
    NerdpackMutationResult,
    NerdpackRemovedTagResponseType,
    NerdpackSubscriptionAccessType,
    NerdpackSubscriptionModel,
    NerdStorageVaultErrorType,
    NerdStorageVaultResultStatus,
    Nr1CatalogAlertConditionType,
    Nr1CatalogInstallerType,
    Nr1CatalogInstallPlanDestination,
    Nr1CatalogInstallPlanDirectiveMode,
    Nr1CatalogInstallPlanOperatingSystem,
    Nr1CatalogInstallPlanTargetType,
    Nr1CatalogMutationResult,
    Nr1CatalogNerdpackVisibility,
    Nr1CatalogQuickstartAlertConditionType,
    Nr1CatalogRenderFormat,
    Nr1CatalogSearchComponentType,
    Nr1CatalogSearchResultType,
    Nr1CatalogSearchSortOption,
    Nr1CatalogSubmitMetadataErrorType,
    Nr1CatalogSupportedEntityTypesMode,
    Nr1CatalogSupportLevel,
    NrqlDropRulesAction,
    NrqlDropRulesErrorReason,
    OrganizationAuthenticationTypeEnum,
    OrganizationProvisioningTypeEnum,
    OrganizationUpdateErrorType,
    PixieLinkPixieProjectErrorType,
    PixieRecordPixieTosAcceptanceErrorType,
    ReferenceEntityCreateRepositoryErrorType,
    RegionScope,
    ServiceLevelEventsQuerySelectFunction,
    ServiceLevelObjectiveRollingTimeWindowUnit,
    StreamingExportStatus,
    SyntheticMonitorStatus,
    SyntheticMonitorType,
    SyntheticsDeviceOrientation,
    SyntheticsDeviceType,
    SyntheticsMonitorCreateErrorType,
    SyntheticsMonitorPeriod,
    SyntheticsMonitorStatus,
    SyntheticsMonitorUpdateErrorType,
    SyntheticsPrivateLocationMutationErrorType,
    SyntheticsStepType,
    TaggingMutationErrorType,
    WhatsNewContentType,
    WorkloadGroupRemainingEntitiesRuleBy,
    WorkloadResultingGroupType,
    WorkloadRollupStrategy,
    WorkloadRuleThresholdType,
    WorkloadStatusSource,
    WorkloadStatusValue,
)
from newrelic_sb_sdk.graphql.input_objects import (
    AccountManagementCreateInput,
    AccountManagementUpdateInput,
    AgentApplicationBrowserSettingsInput,
    AgentApplicationSettingsUpdateInput,
    AgentEnvironmentFilter,
    AiDecisionsRuleBlueprint,
    AiDecisionsSearchBlueprint,
    AiDecisionsSimulationBlueprint,
    AiDecisionsSuggestionBlueprint,
    AiIssuesFilterIncidents,
    AiIssuesFilterIncidentsEvents,
    AiIssuesFilterIssues,
    AiIssuesFilterIssuesEvents,
    AiIssuesGracePeriodConfigurationInput,
    AiNotificationsChannelFilter,
    AiNotificationsChannelInput,
    AiNotificationsChannelSorter,
    AiNotificationsChannelUpdate,
    AiNotificationsConstraint,
    AiNotificationsDestinationFilter,
    AiNotificationsDestinationInput,
    AiNotificationsDestinationSorter,
    AiNotificationsDestinationUpdate,
    AiNotificationsDynamicVariable,
    AiNotificationsSuggestionFilter,
    AiNotificationsVariableFilter,
    AiNotificationsVariableSorter,
    AiTopologyCollectorEdgeBlueprint,
    AiTopologyCollectorVertexBlueprint,
    AiWorkflowsCreateWorkflowInput,
    AiWorkflowsFilters,
    AiWorkflowsTestWorkflowInput,
    AiWorkflowsUpdateWorkflowInput,
    AlertsMutingRuleInput,
    AlertsMutingRuleUpdateInput,
    AlertsNotificationChannelCreateConfiguration,
    AlertsNotificationChannelUpdateConfiguration,
    AlertsNrqlConditionBaselineInput,
    AlertsNrqlConditionsSearchCriteriaInput,
    AlertsNrqlConditionStaticInput,
    AlertsNrqlConditionUpdateBaselineInput,
    AlertsNrqlConditionUpdateStaticInput,
    AlertsPoliciesSearchCriteriaInput,
    AlertsPolicyInput,
    AlertsPolicyUpdateInput,
    ApiAccessCreateInput,
    ApiAccessDeleteInput,
    ApiAccessKeySearchQuery,
    ApiAccessUpdateInput,
    AuthorizationManagementGrantAccess,
    AuthorizationManagementRevokeAccess,
    ChangeTrackingDataHandlingRules,
    ChangeTrackingDeploymentInput,
    ChangeTrackingSearchFilter,
    CloudAwsGovCloudMigrateToAssumeroleInput,
    CloudDisableIntegrationsInput,
    CloudIntegrationsInput,
    CloudLinkCloudAccountsInput,
    CloudRenameAccountsInput,
    CloudUnlinkAccountsInput,
    DashboardInput,
    DashboardLiveUrlsFilterInput,
    DashboardSnapshotUrlInput,
    DashboardUpdatePageInput,
    DashboardUpdateWidgetInput,
    DashboardWidgetInput,
    DataManagementAccountFeatureSettingInput,
    DataManagementRuleInput,
    DomainTypeInput,
    EdgeCreateTraceFilterRulesInput,
    EdgeCreateTraceObserverInput,
    EdgeDeleteTraceFilterRulesInput,
    EdgeDeleteTraceObserverInput,
    EdgeUpdateTraceObserverInput,
    EntityGoldenContextInput,
    EntityGoldenMetricInput,
    EntityGoldenNrqlTimeWindowInput,
    EntityGoldenTagInput,
    EntityRelationshipEdgeFilter,
    EntitySearchOptions,
    EntitySearchQueryBuilder,
    ErrorsInboxAssignErrorGroupInput,
    ErrorsInboxErrorEventInput,
    ErrorsInboxErrorGroupSearchFilterInput,
    ErrorsInboxErrorGroupSortOrderInput,
    ErrorsInboxResourceFilterInput,
    EventsToMetricsCreateRuleInput,
    EventsToMetricsDeleteRuleInput,
    EventsToMetricsUpdateRuleInput,
    InstallationInstallStatusInput,
    InstallationRecipeStatus,
    LogConfigurationsCreateDataPartitionRuleInput,
    LogConfigurationsCreateObfuscationExpressionInput,
    LogConfigurationsCreateObfuscationRuleInput,
    LogConfigurationsParsingRuleConfiguration,
    LogConfigurationsPipelineConfigurationInput,
    LogConfigurationsUpdateDataPartitionRuleInput,
    LogConfigurationsUpdateObfuscationExpressionInput,
    LogConfigurationsUpdateObfuscationRuleInput,
    MetricNormalizationCreateRuleInput,
    MetricNormalizationEditRuleInput,
    NerdpackAllowListInput,
    NerdpackCreationInput,
    NerdpackDataFilter,
    NerdpackOverrideVersionRules,
    NerdpackRemoveVersionTagInput,
    NerdpackSubscribeAccountsInput,
    NerdpackTagVersionInput,
    NerdpackUnsubscribeAccountsInput,
    NerdpackVersionFilter,
    NerdStorageScopeInput,
    NerdStorageVaultScope,
    NerdStorageVaultWriteSecretInput,
    Nr1CatalogSearchFilter,
    Nr1CatalogSubmitMetadataInput,
    NrqlDropRulesCreateDropRuleInput,
    NrqlQueryOptions,
    OrganizationCreateSharedAccountInput,
    OrganizationProvisioningProductInput,
    OrganizationRevokeSharedAccountInput,
    OrganizationUpdateInput,
    OrganizationUpdateSharedAccountInput,
    QueryHistoryQueryHistoryOptionsInput,
    ReferenceEntityCreateRepositoryInput,
    ServiceLevelIndicatorCreateInput,
    ServiceLevelIndicatorUpdateInput,
    SortCriterionWithDirection,
    StreamingExportAwsInput,
    StreamingExportAzureInput,
    StreamingExportRuleInput,
    SyntheticsCreateBrokenLinksMonitorInput,
    SyntheticsCreateCertCheckMonitorInput,
    SyntheticsCreateScriptApiMonitorInput,
    SyntheticsCreateScriptBrowserMonitorInput,
    SyntheticsCreateSimpleBrowserMonitorInput,
    SyntheticsCreateSimpleMonitorInput,
    SyntheticsCreateStepMonitorInput,
    SyntheticsUpdateBrokenLinksMonitorInput,
    SyntheticsUpdateCertCheckMonitorInput,
    SyntheticsUpdateScriptApiMonitorInput,
    SyntheticsUpdateScriptBrowserMonitorInput,
    SyntheticsUpdateSimpleBrowserMonitorInput,
    SyntheticsUpdateSimpleMonitorInput,
    SyntheticsUpdateStepMonitorInput,
    TaggingTagInput,
    TaggingTagValueInput,
    TimeWindowInput,
    UserManagementCreateGroup,
    UserManagementCreateUser,
    UserManagementDeleteGroup,
    UserManagementDeleteUser,
    UserManagementGroupFilterInput,
    UserManagementUpdateGroup,
    UserManagementUpdateUser,
    UserManagementUserFilterInput,
    UserManagementUsersGroupsInput,
    UsersUserSearchQuery,
    WhatsNewContentSearchQuery,
    WorkloadCreateInput,
    WorkloadDuplicateInput,
    WorkloadUpdateInput,
)
from newrelic_sb_sdk.graphql.scalars import (
    ID,
    AgentApplicationSettingsErrorCollectorHttpStatus,
    AgentApplicationSettingsRawJsConfiguration,
    AiDecisionsRuleExpression,
    AttributeMap,
    Boolean,
    DashboardWidgetRawConfiguration,
    Date,
    DateTime,
    DistributedTracingSpanAttributes,
    EntityAlertViolationInt,
    EntityGuid,
    EpochMilliseconds,
    EpochSeconds,
    Float,
    InstallationRawMetadata,
    Int,
    LogConfigurationsLogDataPartitionName,
    Milliseconds,
    Minutes,
    NerdpackTagName,
    NerdStorageDocument,
    Nr1CatalogRawNerdletState,
    NrdbRawResults,
    NrdbResult,
    Nrql,
    Seconds,
    SecureValue,
    SemVer,
    String,
)

from . import nerdgraph

__docformat__ = "markdown"


class AiIssuesIIncident(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_ids",
        "closed_at",
        "created_at",
        "description",
        "entity_guids",
        "entity_names",
        "entity_types",
        "environment_id",
        "incident_id",
        "priority",
        "state",
        "timestamp",
        "title",
        "updated_at",
    )
    account_ids = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="accountIds"
    )

    closed_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="closedAt")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    description = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="description",
    )

    entity_guids = sgqlc.types.Field(EntityGuid, graphql_name="entityGuids")

    entity_names = sgqlc.types.Field(String, graphql_name="entityNames")

    entity_types = sgqlc.types.Field(String, graphql_name="entityTypes")

    environment_id = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="environmentId"
    )

    incident_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="incidentId")

    priority = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesPriority), graphql_name="priority"
    )

    state = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesIncidentState), graphql_name="state"
    )

    timestamp = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="timestamp"
    )

    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="title")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="updatedAt"
    )


class AiWorkflowsResponseError(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("description",)
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )


class AlertableEntity(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("alert_severity", "alert_violations", "recent_alert_violations")
    alert_severity = sgqlc.types.Field(
        EntityAlertSeverity, graphql_name="alertSeverity"
    )

    alert_violations = sgqlc.types.Field(
        sgqlc.types.list_of("EntityAlertViolation"),
        graphql_name="alertViolations",
        args=sgqlc.types.ArgDict(
            (
                (
                    "end_time",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EpochMilliseconds),
                        graphql_name="endTime",
                        default=None,
                    ),
                ),
                (
                    "start_time",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EpochMilliseconds),
                        graphql_name="startTime",
                        default=None,
                    ),
                ),
            )
        ),
    )

    recent_alert_violations = sgqlc.types.Field(
        sgqlc.types.list_of("EntityAlertViolation"),
        graphql_name="recentAlertViolations",
        args=sgqlc.types.ArgDict(
            (("count", sgqlc.types.Arg(Int, graphql_name="count", default=10)),)
        ),
    )
    """Arguments:

    * `count` (`Int`) (default: `10`)
    """


class AlertableEntityOutline(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("alert_severity",)
    alert_severity = sgqlc.types.Field(
        EntityAlertSeverity, graphql_name="alertSeverity"
    )


class AlertsNotificationChannel(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("associated_policies", "id", "name", "type")
    associated_policies = sgqlc.types.Field(
        sgqlc.types.non_null("AlertsNotificationChannelPoliciesResultSet"),
        graphql_name="associatedPolicies",
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNotificationChannelType), graphql_name="type"
    )


class AlertsNrqlCondition(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = (
        "description",
        "enabled",
        "entity",
        "entity_guid",
        "expiration",
        "id",
        "name",
        "nrql",
        "policy_id",
        "runbook_url",
        "signal",
        "terms",
        "type",
        "violation_time_limit_seconds",
    )
    description = sgqlc.types.Field(String, graphql_name="description")

    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    entity = sgqlc.types.Field("EntityOutline", graphql_name="entity")

    entity_guid = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGuid), graphql_name="entityGuid"
    )

    expiration = sgqlc.types.Field(
        sgqlc.types.non_null("AlertsNrqlConditionExpiration"), graphql_name="expiration"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    nrql = sgqlc.types.Field(
        sgqlc.types.non_null("AlertsNrqlConditionQuery"), graphql_name="nrql"
    )

    policy_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="policyId")

    runbook_url = sgqlc.types.Field(String, graphql_name="runbookUrl")

    signal = sgqlc.types.Field(
        sgqlc.types.non_null("AlertsNrqlConditionSignal"), graphql_name="signal"
    )

    terms = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AlertsNrqlConditionTerms"))
        ),
        graphql_name="terms",
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNrqlConditionType), graphql_name="type"
    )

    violation_time_limit_seconds = sgqlc.types.Field(
        Seconds, graphql_name="violationTimeLimitSeconds"
    )


class ApiAccessKey(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("created_at", "id", "key", "name", "notes", "type")
    created_at = sgqlc.types.Field(EpochSeconds, graphql_name="createdAt")

    id = sgqlc.types.Field(ID, graphql_name="id")

    key = sgqlc.types.Field(String, graphql_name="key")

    name = sgqlc.types.Field(String, graphql_name="name")

    notes = sgqlc.types.Field(String, graphql_name="notes")

    type = sgqlc.types.Field(ApiAccessKeyType, graphql_name="type")


class ApiAccessKeyError(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(String, graphql_name="message")

    type = sgqlc.types.Field(ApiAccessKeyType, graphql_name="type")


class ApmBrowserApplicationEntity(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("apm_browser_summary",)
    apm_browser_summary = sgqlc.types.Field(
        "ApmBrowserApplicationSummaryData", graphql_name="apmBrowserSummary"
    )


class ApmBrowserApplicationEntityOutline(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("apm_browser_summary",)
    apm_browser_summary = sgqlc.types.Field(
        "ApmBrowserApplicationSummaryData", graphql_name="apmBrowserSummary"
    )


class CloudIntegration(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "id",
        "linked_account",
        "name",
        "nr_account_id",
        "service",
        "updated_at",
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochSeconds), graphql_name="createdAt"
    )

    id = sgqlc.types.Field(Int, graphql_name="id")

    linked_account = sgqlc.types.Field(
        "CloudLinkedAccount", graphql_name="linkedAccount"
    )

    name = sgqlc.types.Field(String, graphql_name="name")

    nr_account_id = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="nrAccountId"
    )

    service = sgqlc.types.Field("CloudService", graphql_name="service")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochSeconds), graphql_name="updatedAt"
    )


class CloudProvider(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "icon",
        "id",
        "name",
        "service",
        "services",
        "slug",
        "updated_at",
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochSeconds), graphql_name="createdAt"
    )

    icon = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="icon")

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    service = sgqlc.types.Field(
        "CloudService",
        graphql_name="service",
        args=sgqlc.types.ArgDict(
            (
                (
                    "slug",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="slug", default=None
                    ),
                ),
            )
        ),
    )

    services = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("CloudService"))),
        graphql_name="services",
    )

    slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="slug")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochSeconds), graphql_name="updatedAt"
    )


class CollectionEntity(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("collection", "guid")
    collection = sgqlc.types.Field(
        "EntityCollection",
        graphql_name="collection",
        args=sgqlc.types.ArgDict(
            (
                (
                    "name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="name", default=None
                    ),
                ),
            )
        ),
    )

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")


class EdgeEndpointDetail(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("host", "port")
    host = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="host")

    port = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="port")


class EntityRelationshipEdge(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("created_at", "source", "target", "type")
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    source = sgqlc.types.Field(
        sgqlc.types.non_null("EntityRelationshipVertex"), graphql_name="source"
    )

    target = sgqlc.types.Field(
        sgqlc.types.non_null("EntityRelationshipVertex"), graphql_name="target"
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(EntityRelationshipEdgeType), graphql_name="type"
    )


class ErrorsInboxResource(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("id", "url")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class ErrorsInboxResponseError(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("description",)
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )


class InfrastructureIntegrationEntity(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("integration_type_code",)
    integration_type_code = sgqlc.types.Field(
        String, graphql_name="integrationTypeCode"
    )


class InfrastructureIntegrationEntityOutline(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("integration_type_code",)
    integration_type_code = sgqlc.types.Field(
        String, graphql_name="integrationTypeCode"
    )


class Nr1CatalogInstallPlanDirective(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("mode",)
    mode = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogInstallPlanDirectiveMode), graphql_name="mode"
    )


class Nr1CatalogInstaller(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("type",)
    type = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogInstallerType), graphql_name="type"
    )


class Nr1CatalogNerdpackItem(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("id", "metadata")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    metadata = sgqlc.types.Field(
        "Nr1CatalogNerdpackItemMetadata", graphql_name="metadata"
    )


class Nr1CatalogNerdpackItemMetadata(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("description", "display_name", "previews")
    description = sgqlc.types.Field(String, graphql_name="description")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    previews = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("Nr1CatalogPreview"))
        ),
        graphql_name="previews",
    )


class Nr1CatalogPreview(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("url",)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class Nr1CatalogQuickstartComponent(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("metadata",)
    metadata = sgqlc.types.Field(
        sgqlc.types.non_null("Nr1CatalogQuickstartComponentMetadata"),
        graphql_name="metadata",
    )


class Nr1CatalogQuickstartComponentMetadata(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("description", "display_name")
    description = sgqlc.types.Field(String, graphql_name="description")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")


class Nr1CatalogSupportedEntityTypes(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("mode",)
    mode = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogSupportedEntityTypesMode), graphql_name="mode"
    )


class SuggestedNrqlQuery(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("nrql", "title")
    nrql = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="nrql")

    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="title")


class WhatsNewContent(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = (
        "content_type",
        "context",
        "id",
        "publish_date",
        "summary",
        "title",
    )
    content_type = sgqlc.types.Field(
        sgqlc.types.non_null(WhatsNewContentType), graphql_name="contentType"
    )

    context = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="context"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    publish_date = sgqlc.types.Field(EpochMilliseconds, graphql_name="publishDate")

    summary = sgqlc.types.Field(String, graphql_name="summary")

    title = sgqlc.types.Field(String, graphql_name="title")


class WorkloadStatusResult(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = ("source", "value")
    source = sgqlc.types.Field(
        sgqlc.types.non_null(WorkloadStatusSource), graphql_name="source"
    )

    value = sgqlc.types.Field(
        sgqlc.types.non_null(WorkloadStatusValue), graphql_name="value"
    )


class Entity(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = (
        "account",
        "account_id",
        "alert_severity",
        "alert_violations",
        "deployment_search",
        "domain",
        "entity_type",
        "first_indexed_at",
        "golden_metrics",
        "golden_tags",
        "guid",
        "indexed_at",
        "last_reporting_change_at",
        "name",
        "nerd_storage",
        "nrdb_query",
        "permalink",
        "recent_alert_violations",
        "related_entities",
        "reporting",
        "service_level",
        "tags",
        "tags_with_metadata",
        "tracing_summary",
        "type",
    )
    account = sgqlc.types.Field("AccountOutline", graphql_name="account")

    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    alert_severity = sgqlc.types.Field(
        EntityAlertSeverity, graphql_name="alertSeverity"
    )

    alert_violations = sgqlc.types.Field(
        sgqlc.types.list_of("EntityAlertViolation"),
        graphql_name="alertViolations",
        args=sgqlc.types.ArgDict(
            (
                (
                    "end_time",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EpochMilliseconds),
                        graphql_name="endTime",
                        default=None,
                    ),
                ),
                (
                    "start_time",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EpochMilliseconds),
                        graphql_name="startTime",
                        default=None,
                    ),
                ),
            )
        ),
    )

    deployment_search = sgqlc.types.Field(
        "ChangeTrackingDeploymentSearchResult",
        graphql_name="deploymentSearch",
        args=sgqlc.types.ArgDict(
            (
                (
                    "filter",
                    sgqlc.types.Arg(
                        ChangeTrackingSearchFilter, graphql_name="filter", default=None
                    ),
                ),
            )
        ),
    )

    domain = sgqlc.types.Field(String, graphql_name="domain")

    entity_type = sgqlc.types.Field(EntityType, graphql_name="entityType")

    first_indexed_at = sgqlc.types.Field(
        EpochMilliseconds, graphql_name="firstIndexedAt"
    )

    golden_metrics = sgqlc.types.Field(
        "EntityGoldenContextScopedGoldenMetrics",
        graphql_name="goldenMetrics",
        args=sgqlc.types.ArgDict(
            (
                (
                    "context",
                    sgqlc.types.Arg(
                        EntityGoldenContextInput, graphql_name="context", default=None
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        EntityGoldenNrqlTimeWindowInput,
                        graphql_name="timeWindow",
                        default=None,
                    ),
                ),
            )
        ),
    )

    golden_tags = sgqlc.types.Field(
        "EntityGoldenContextScopedGoldenTags",
        graphql_name="goldenTags",
        args=sgqlc.types.ArgDict(
            (
                (
                    "context",
                    sgqlc.types.Arg(
                        EntityGoldenContextInput, graphql_name="context", default=None
                    ),
                ),
            )
        ),
    )

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    indexed_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="indexedAt")

    last_reporting_change_at = sgqlc.types.Field(
        EpochMilliseconds, graphql_name="lastReportingChangeAt"
    )

    name = sgqlc.types.Field(String, graphql_name="name")

    nerd_storage = sgqlc.types.Field(
        "NerdStorageEntityScope", graphql_name="nerdStorage"
    )

    nrdb_query = sgqlc.types.Field(
        "NrdbResultContainer",
        graphql_name="nrdbQuery",
        args=sgqlc.types.ArgDict(
            (
                (
                    "async_",
                    sgqlc.types.Arg(Boolean, graphql_name="async", default=False),
                ),
                (
                    "nrql",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Nrql), graphql_name="nrql", default=None
                    ),
                ),
                (
                    "options",
                    sgqlc.types.Arg(
                        NrqlQueryOptions, graphql_name="options", default=None
                    ),
                ),
                (
                    "timeout",
                    sgqlc.types.Arg(Seconds, graphql_name="timeout", default=None),
                ),
            )
        ),
    )

    permalink = sgqlc.types.Field(String, graphql_name="permalink")

    recent_alert_violations = sgqlc.types.Field(
        sgqlc.types.list_of("EntityAlertViolation"),
        graphql_name="recentAlertViolations",
        args=sgqlc.types.ArgDict(
            (("count", sgqlc.types.Arg(Int, graphql_name="count", default=None)),)
        ),
    )

    related_entities = sgqlc.types.Field(
        "EntityRelationshipRelatedEntitiesResult",
        graphql_name="relatedEntities",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        EntityRelationshipEdgeFilter,
                        graphql_name="filter",
                        default=None,
                    ),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
            )
        ),
    )

    reporting = sgqlc.types.Field(Boolean, graphql_name="reporting")

    service_level = sgqlc.types.Field(
        "ServiceLevelDefinition", graphql_name="serviceLevel"
    )

    tags = sgqlc.types.Field(sgqlc.types.list_of("EntityTag"), graphql_name="tags")

    tags_with_metadata = sgqlc.types.Field(
        sgqlc.types.list_of("EntityTagWithMetadata"), graphql_name="tagsWithMetadata"
    )

    tracing_summary = sgqlc.types.Field(
        "DistributedTracingEntityTracingSummary",
        graphql_name="tracingSummary",
        args=sgqlc.types.ArgDict(
            (
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )

    type = sgqlc.types.Field(String, graphql_name="type")


class EntityOutline(sgqlc.types.Interface):
    __schema__ = nerdgraph
    __field_names__ = (
        "account",
        "account_id",
        "alert_severity",
        "domain",
        "entity_type",
        "first_indexed_at",
        "golden_metrics",
        "golden_tags",
        "guid",
        "indexed_at",
        "last_reporting_change_at",
        "name",
        "permalink",
        "reporting",
        "service_level",
        "tags",
        "type",
    )
    account = sgqlc.types.Field("AccountOutline", graphql_name="account")

    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    alert_severity = sgqlc.types.Field(
        EntityAlertSeverity, graphql_name="alertSeverity"
    )

    domain = sgqlc.types.Field(String, graphql_name="domain")

    entity_type = sgqlc.types.Field(EntityType, graphql_name="entityType")

    first_indexed_at = sgqlc.types.Field(
        EpochMilliseconds, graphql_name="firstIndexedAt"
    )

    golden_metrics = sgqlc.types.Field(
        "EntityGoldenContextScopedGoldenMetrics",
        graphql_name="goldenMetrics",
        args=sgqlc.types.ArgDict(
            (
                (
                    "context",
                    sgqlc.types.Arg(
                        EntityGoldenContextInput, graphql_name="context", default=None
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        EntityGoldenNrqlTimeWindowInput,
                        graphql_name="timeWindow",
                        default=None,
                    ),
                ),
            )
        ),
    )

    golden_tags = sgqlc.types.Field(
        "EntityGoldenContextScopedGoldenTags",
        graphql_name="goldenTags",
        args=sgqlc.types.ArgDict(
            (
                (
                    "context",
                    sgqlc.types.Arg(
                        EntityGoldenContextInput, graphql_name="context", default=None
                    ),
                ),
            )
        ),
    )

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    indexed_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="indexedAt")

    last_reporting_change_at = sgqlc.types.Field(
        EpochMilliseconds, graphql_name="lastReportingChangeAt"
    )

    name = sgqlc.types.Field(String, graphql_name="name")

    permalink = sgqlc.types.Field(String, graphql_name="permalink")

    reporting = sgqlc.types.Field(Boolean, graphql_name="reporting")

    service_level = sgqlc.types.Field(
        "ServiceLevelDefinition", graphql_name="serviceLevel"
    )

    tags = sgqlc.types.Field(sgqlc.types.list_of("EntityTag"), graphql_name="tags")

    type = sgqlc.types.Field(String, graphql_name="type")


class Account(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "agent_environment",
        "ai_decisions",
        "ai_issues",
        "ai_notifications",
        "ai_topology",
        "ai_workflows",
        "alerts",
        "cloud",
        "data_management",
        "edge",
        "events_to_metrics",
        "historical_data_export",
        "id",
        "incident_intelligence_environment",
        "installation",
        "log_configurations",
        "metric_normalization",
        "name",
        "nerd_storage",
        "nrql",
        "nrql_drop_rules",
        "pixie",
        "streaming_export",
        "synthetics",
        "workload",
    )
    agent_environment = sgqlc.types.Field(
        "AgentEnvironmentAccountStitchedFields", graphql_name="agentEnvironment"
    )

    ai_decisions = sgqlc.types.Field(
        "AiDecisionsAccountStitchedFields", graphql_name="aiDecisions"
    )

    ai_issues = sgqlc.types.Field(
        "AiIssuesAccountStitchedFields", graphql_name="aiIssues"
    )

    ai_notifications = sgqlc.types.Field(
        "AiNotificationsAccountStitchedFields", graphql_name="aiNotifications"
    )

    ai_topology = sgqlc.types.Field(
        "AiTopologyAccountStitchedFields", graphql_name="aiTopology"
    )

    ai_workflows = sgqlc.types.Field(
        "AiWorkflowsAccountStitchedFields", graphql_name="aiWorkflows"
    )

    alerts = sgqlc.types.Field("AlertsAccountStitchedFields", graphql_name="alerts")

    cloud = sgqlc.types.Field("CloudAccountFields", graphql_name="cloud")

    data_management = sgqlc.types.Field(
        "DataManagementAccountStitchedFields", graphql_name="dataManagement"
    )

    edge = sgqlc.types.Field("EdgeAccountStitchedFields", graphql_name="edge")

    events_to_metrics = sgqlc.types.Field(
        "EventsToMetricsAccountStitchedFields", graphql_name="eventsToMetrics"
    )

    historical_data_export = sgqlc.types.Field(
        "HistoricalDataExportAccountStitchedFields", graphql_name="historicalDataExport"
    )

    id = sgqlc.types.Field(Int, graphql_name="id")

    incident_intelligence_environment = sgqlc.types.Field(
        "IncidentIntelligenceEnvironmentAccountStitchedFields",
        graphql_name="incidentIntelligenceEnvironment",
    )

    installation = sgqlc.types.Field(
        "InstallationAccountStitchedFields", graphql_name="installation"
    )

    log_configurations = sgqlc.types.Field(
        "LogConfigurationsAccountStitchedFields", graphql_name="logConfigurations"
    )

    metric_normalization = sgqlc.types.Field(
        "MetricNormalizationAccountStitchedFields", graphql_name="metricNormalization"
    )

    name = sgqlc.types.Field(String, graphql_name="name")

    nerd_storage = sgqlc.types.Field(
        "NerdStorageAccountScope", graphql_name="nerdStorage"
    )

    nrql = sgqlc.types.Field(
        "NrdbResultContainer",
        graphql_name="nrql",
        args=sgqlc.types.ArgDict(
            (
                (
                    "async_",
                    sgqlc.types.Arg(Boolean, graphql_name="async", default=False),
                ),
                (
                    "options",
                    sgqlc.types.Arg(
                        NrqlQueryOptions, graphql_name="options", default=None
                    ),
                ),
                (
                    "query",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Nrql), graphql_name="query", default=None
                    ),
                ),
                (
                    "timeout",
                    sgqlc.types.Arg(Seconds, graphql_name="timeout", default=None),
                ),
            )
        ),
    )

    nrql_drop_rules = sgqlc.types.Field(
        "NrqlDropRulesAccountStitchedFields", graphql_name="nrqlDropRules"
    )

    pixie = sgqlc.types.Field("PixieAccountStitchedFields", graphql_name="pixie")

    streaming_export = sgqlc.types.Field(
        "StreamingExportAccountStitchedFields", graphql_name="streamingExport"
    )

    synthetics = sgqlc.types.Field(
        "SyntheticsAccountStitchedFields", graphql_name="synthetics"
    )

    workload = sgqlc.types.Field(
        "WorkloadAccountStitchedFields", graphql_name="workload"
    )


class AccountManagementCreateResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("managed_account",)
    managed_account = sgqlc.types.Field(
        "AccountManagementManagedAccount", graphql_name="managedAccount"
    )


class AccountManagementManagedAccount(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "is_canceled", "name", "region_code")
    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    is_canceled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="isCanceled"
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    region_code = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="regionCode"
    )


class AccountManagementOrganizationStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("managed_accounts",)
    managed_accounts = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(AccountManagementManagedAccount)),
        graphql_name="managedAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "is_canceled",
                    sgqlc.types.Arg(Boolean, graphql_name="isCanceled", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `is_canceled` (`Boolean`)
    """


class AccountManagementUpdateResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("managed_account",)
    managed_account = sgqlc.types.Field(
        AccountManagementManagedAccount, graphql_name="managedAccount"
    )


class AccountOutline(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "name", "reporting_event_types")
    id = sgqlc.types.Field(Int, graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    reporting_event_types = sgqlc.types.Field(
        sgqlc.types.list_of(String),
        graphql_name="reportingEventTypes",
        args=sgqlc.types.ArgDict(
            (
                (
                    "filter",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(String), graphql_name="filter", default=None
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `filter` (`[String]`)
    * `time_window` (`TimeWindowInput`)
    """


class AccountReference(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "name")
    id = sgqlc.types.Field(Int, graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")


class Actor(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account",
        "accounts",
        "api_access",
        "cloud",
        "dashboard",
        "distributed_tracing",
        "entities",
        "entity",
        "entity_search",
        "errors_inbox",
        "incident_intelligence_environment",
        "mobile_push_notification",
        "nerd_storage",
        "nerd_storage_vault",
        "nerdpacks",
        "nr1_catalog",
        "nrql",
        "organization",
        "pixie",
        "query_history",
        "user",
        "users",
    )
    account = sgqlc.types.Field(
        Account,
        graphql_name="account",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    accounts = sgqlc.types.Field(
        sgqlc.types.list_of(AccountOutline),
        graphql_name="accounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "scope",
                    sgqlc.types.Arg(
                        RegionScope, graphql_name="scope", default="IN_REGION"
                    ),
                ),
            )
        ),
    )

    api_access = sgqlc.types.Field(
        "ApiAccessActorStitchedFields", graphql_name="apiAccess"
    )

    cloud = sgqlc.types.Field("CloudActorFields", graphql_name="cloud")

    dashboard = sgqlc.types.Field(
        "DashboardActorStitchedFields", graphql_name="dashboard"
    )

    distributed_tracing = sgqlc.types.Field(
        "DistributedTracingActorStitchedFields", graphql_name="distributedTracing"
    )

    entities = sgqlc.types.Field(
        sgqlc.types.list_of(Entity),
        graphql_name="entities",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(EntityGuid)),
                        graphql_name="guids",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `guids` (`[EntityGuid]!`)
    """

    entity = sgqlc.types.Field(
        Entity,
        graphql_name="entity",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    entity_search = sgqlc.types.Field(
        "EntitySearch",
        graphql_name="entitySearch",
        args=sgqlc.types.ArgDict(
            (
                (
                    "options",
                    sgqlc.types.Arg(
                        EntitySearchOptions, graphql_name="options", default=None
                    ),
                ),
                ("query", sgqlc.types.Arg(String, graphql_name="query", default=None)),
                (
                    "query_builder",
                    sgqlc.types.Arg(
                        EntitySearchQueryBuilder,
                        graphql_name="queryBuilder",
                        default=None,
                    ),
                ),
                (
                    "sort_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(EntitySearchSortCriteria),
                        graphql_name="sortBy",
                        default=("NAME",),
                    ),
                ),
                (
                    "sort_by_with_direction",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(SortCriterionWithDirection),
                        graphql_name="sortByWithDirection",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `options` (`EntitySearchOptions`)
    * `query` (`String`)
    * `query_builder` (`EntitySearchQueryBuilder`)
    * `sort_by` (`[EntitySearchSortCriteria]`) (default: `[NAME]`)
    * `sort_by_with_direction` (`[SortCriterionWithDirection]`)
    """

    errors_inbox = sgqlc.types.Field(
        "ErrorsInboxActorStitchedFields", graphql_name="errorsInbox"
    )

    incident_intelligence_environment = sgqlc.types.Field(
        "IncidentIntelligenceEnvironmentActorStitchedFields",
        graphql_name="incidentIntelligenceEnvironment",
    )

    mobile_push_notification = sgqlc.types.Field(
        "MobilePushNotificationActorStitchedFields",
        graphql_name="mobilePushNotification",
    )

    nerd_storage = sgqlc.types.Field(
        "NerdStorageActorScope", graphql_name="nerdStorage"
    )

    nerd_storage_vault = sgqlc.types.Field(
        "NerdStorageVaultActorStitchedFields", graphql_name="nerdStorageVault"
    )

    nerdpacks = sgqlc.types.Field("NerdpackNerdpacks", graphql_name="nerdpacks")

    nr1_catalog = sgqlc.types.Field(
        "Nr1CatalogActorStitchedFields", graphql_name="nr1Catalog"
    )

    nrql = sgqlc.types.Field(
        "CrossAccountNrdbResultContainer",
        graphql_name="nrql",
        args=sgqlc.types.ArgDict(
            (
                (
                    "accounts",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(Int))
                        ),
                        graphql_name="accounts",
                        default=None,
                    ),
                ),
                (
                    "async_",
                    sgqlc.types.Arg(Boolean, graphql_name="async", default=False),
                ),
                (
                    "options",
                    sgqlc.types.Arg(
                        NrqlQueryOptions, graphql_name="options", default=None
                    ),
                ),
                (
                    "query",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Nrql), graphql_name="query", default=None
                    ),
                ),
                (
                    "timeout",
                    sgqlc.types.Arg(Seconds, graphql_name="timeout", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `accounts` (`[Int!]!`)
    * `async_` (`Boolean`) (default: `false`)
    * `options` (`NrqlQueryOptions`)
    * `query` (`Nrql!`)
    * `timeout` (`Seconds`)
    """

    organization = sgqlc.types.Field("Organization", graphql_name="organization")

    pixie = sgqlc.types.Field("PixieActorStitchedFields", graphql_name="pixie")

    query_history = sgqlc.types.Field(
        "QueryHistoryActorStitchedFields", graphql_name="queryHistory"
    )

    user = sgqlc.types.Field("User", graphql_name="user")

    users = sgqlc.types.Field("UsersActorStitchedFields", graphql_name="users")


class AgentApplicationApmBrowserSettings(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("cookies_enabled", "distributed_tracing_enabled", "loader_type")
    cookies_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="cookiesEnabled"
    )

    distributed_tracing_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="distributedTracingEnabled"
    )

    loader_type = sgqlc.types.Field(
        sgqlc.types.non_null(AgentApplicationBrowserLoader), graphql_name="loaderType"
    )


class AgentApplicationBrowserSettings(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "cookies_enabled",
        "distributed_tracing_enabled",
        "loader_script",
        "loader_type",
    )
    cookies_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="cookiesEnabled"
    )

    distributed_tracing_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="distributedTracingEnabled"
    )

    loader_script = sgqlc.types.Field(String, graphql_name="loaderScript")

    loader_type = sgqlc.types.Field(
        sgqlc.types.non_null(AgentApplicationBrowserLoader), graphql_name="loaderType"
    )


class AgentApplicationCreateBrowserResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("guid", "name", "settings")
    guid = sgqlc.types.Field(sgqlc.types.non_null(EntityGuid), graphql_name="guid")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    settings = sgqlc.types.Field(
        AgentApplicationBrowserSettings, graphql_name="settings"
    )


class AgentApplicationCreateMobileResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "application_token",
        "entity_outline",
        "guid",
        "name",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    application_token = sgqlc.types.Field(
        sgqlc.types.non_null(SecureValue), graphql_name="applicationToken"
    )

    entity_outline = sgqlc.types.Field(EntityOutline, graphql_name="entityOutline")

    guid = sgqlc.types.Field(sgqlc.types.non_null(EntityGuid), graphql_name="guid")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class AgentApplicationDeleteResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("success",)
    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="success")


class AgentApplicationEnableBrowserResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("name", "settings")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    settings = sgqlc.types.Field(
        AgentApplicationApmBrowserSettings, graphql_name="settings"
    )


class AgentApplicationSettingsApmBase(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "alias",
        "apm_config",
        "capture_memcache_keys",
        "error_collector",
        "jfr",
        "original_name",
        "slow_sql",
        "thread_profiler",
        "tracer_type",
        "transaction_tracer",
    )
    alias = sgqlc.types.Field(String, graphql_name="alias")

    apm_config = sgqlc.types.Field(
        sgqlc.types.non_null("AgentApplicationSettingsApmConfig"),
        graphql_name="apmConfig",
    )

    capture_memcache_keys = sgqlc.types.Field(
        Boolean, graphql_name="captureMemcacheKeys"
    )

    error_collector = sgqlc.types.Field(
        "AgentApplicationSettingsErrorCollector", graphql_name="errorCollector"
    )

    jfr = sgqlc.types.Field("AgentApplicationSettingsJfr", graphql_name="jfr")

    original_name = sgqlc.types.Field(String, graphql_name="originalName")

    slow_sql = sgqlc.types.Field(
        "AgentApplicationSettingsSlowSql", graphql_name="slowSql"
    )

    thread_profiler = sgqlc.types.Field(
        "AgentApplicationSettingsThreadProfiler", graphql_name="threadProfiler"
    )

    tracer_type = sgqlc.types.Field(
        AgentApplicationSettingsTracer, graphql_name="tracerType"
    )

    transaction_tracer = sgqlc.types.Field(
        "AgentApplicationSettingsTransactionTracer", graphql_name="transactionTracer"
    )


class AgentApplicationSettingsApmConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("apdex_target", "use_server_side_config")
    apdex_target = sgqlc.types.Field(Float, graphql_name="apdexTarget")

    use_server_side_config = sgqlc.types.Field(
        Boolean, graphql_name="useServerSideConfig"
    )


class AgentApplicationSettingsBrowserAjax(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("deny_list",)
    deny_list = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="denyList"
    )


class AgentApplicationSettingsBrowserBase(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("browser_config", "browser_monitoring")
    browser_config = sgqlc.types.Field(
        sgqlc.types.non_null("AgentApplicationSettingsBrowserConfig"),
        graphql_name="browserConfig",
    )

    browser_monitoring = sgqlc.types.Field(
        sgqlc.types.non_null("AgentApplicationSettingsBrowserMonitoring"),
        graphql_name="browserMonitoring",
    )


class AgentApplicationSettingsBrowserConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("apdex_target",)
    apdex_target = sgqlc.types.Field(Float, graphql_name="apdexTarget")


class AgentApplicationSettingsBrowserDistributedTracing(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "allowed_origins",
        "cors_enabled",
        "cors_use_newrelic_header",
        "cors_use_tracecontext_headers",
        "enabled",
        "exclude_newrelic_header",
    )
    allowed_origins = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="allowedOrigins"
    )

    cors_enabled = sgqlc.types.Field(Boolean, graphql_name="corsEnabled")

    cors_use_newrelic_header = sgqlc.types.Field(
        Boolean, graphql_name="corsUseNewrelicHeader"
    )

    cors_use_tracecontext_headers = sgqlc.types.Field(
        Boolean, graphql_name="corsUseTracecontextHeaders"
    )

    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")

    exclude_newrelic_header = sgqlc.types.Field(
        Boolean, graphql_name="excludeNewrelicHeader"
    )


class AgentApplicationSettingsBrowserMonitoring(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("ajax", "distributed_tracing", "loader", "privacy")
    ajax = sgqlc.types.Field(AgentApplicationSettingsBrowserAjax, graphql_name="ajax")

    distributed_tracing = sgqlc.types.Field(
        sgqlc.types.non_null(AgentApplicationSettingsBrowserDistributedTracing),
        graphql_name="distributedTracing",
    )

    loader = sgqlc.types.Field(
        sgqlc.types.non_null(AgentApplicationSettingsBrowserLoader),
        graphql_name="loader",
    )

    privacy = sgqlc.types.Field(
        sgqlc.types.non_null("AgentApplicationSettingsBrowserPrivacy"),
        graphql_name="privacy",
    )


class AgentApplicationSettingsBrowserPrivacy(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("cookies_enabled",)
    cookies_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="cookiesEnabled"
    )


class AgentApplicationSettingsBrowserProperties(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("js_config", "js_config_script", "js_loader_script")
    js_config = sgqlc.types.Field(
        AgentApplicationSettingsRawJsConfiguration, graphql_name="jsConfig"
    )

    js_config_script = sgqlc.types.Field(String, graphql_name="jsConfigScript")

    js_loader_script = sgqlc.types.Field(String, graphql_name="jsLoaderScript")


class AgentApplicationSettingsErrorCollector(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "enabled",
        "expected_error_classes",
        "expected_error_codes",
        "ignored_error_classes",
        "ignored_error_codes",
    )
    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")

    expected_error_classes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="expectedErrorClasses",
    )

    expected_error_codes = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(AgentApplicationSettingsErrorCollectorHttpStatus)
        ),
        graphql_name="expectedErrorCodes",
    )

    ignored_error_classes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="ignoredErrorClasses",
    )

    ignored_error_codes = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(AgentApplicationSettingsErrorCollectorHttpStatus)
        ),
        graphql_name="ignoredErrorCodes",
    )


class AgentApplicationSettingsIgnoredStatusCodeRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("hosts", "status_codes")
    hosts = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="hosts"
    )

    status_codes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="statusCodes"
    )


class AgentApplicationSettingsJfr(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("enabled",)
    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")


class AgentApplicationSettingsMobileBase(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("network_settings", "use_crash_reports")
    network_settings = sgqlc.types.Field(
        "AgentApplicationSettingsMobileNetworkSettings", graphql_name="networkSettings"
    )

    use_crash_reports = sgqlc.types.Field(Boolean, graphql_name="useCrashReports")


class AgentApplicationSettingsMobileNetworkSettings(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "aliases",
        "filter_mode",
        "hide_list",
        "ignored_status_code_rules",
        "show_list",
    )
    aliases = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("AgentApplicationSettingsNetworkAlias")
        ),
        graphql_name="aliases",
    )

    filter_mode = sgqlc.types.Field(
        AgentApplicationSettingsNetworkFilterMode, graphql_name="filterMode"
    )

    hide_list = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="hideList"
    )

    ignored_status_code_rules = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(AgentApplicationSettingsIgnoredStatusCodeRule)
        ),
        graphql_name="ignoredStatusCodeRules",
    )

    show_list = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="showList"
    )


class AgentApplicationSettingsMobileProperties(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("application_token",)
    application_token = sgqlc.types.Field(SecureValue, graphql_name="applicationToken")


class AgentApplicationSettingsNetworkAlias(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("alias", "hosts")
    alias = sgqlc.types.Field(String, graphql_name="alias")

    hosts = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="hosts"
    )


class AgentApplicationSettingsSlowSql(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("enabled",)
    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")


class AgentApplicationSettingsThreadProfiler(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("enabled",)
    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")


class AgentApplicationSettingsTransactionTracer(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "capture_memcache_keys",
        "enabled",
        "explain_enabled",
        "explain_threshold_type",
        "explain_threshold_value",
        "log_sql",
        "record_sql",
        "stack_trace_threshold",
        "transaction_threshold_type",
        "transaction_threshold_value",
    )
    capture_memcache_keys = sgqlc.types.Field(
        Boolean, graphql_name="captureMemcacheKeys"
    )

    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")

    explain_enabled = sgqlc.types.Field(Boolean, graphql_name="explainEnabled")

    explain_threshold_type = sgqlc.types.Field(
        AgentApplicationSettingsThresholdTypeEnum, graphql_name="explainThresholdType"
    )

    explain_threshold_value = sgqlc.types.Field(
        Seconds, graphql_name="explainThresholdValue"
    )

    log_sql = sgqlc.types.Field(Boolean, graphql_name="logSql")

    record_sql = sgqlc.types.Field(
        AgentApplicationSettingsRecordSqlEnum, graphql_name="recordSql"
    )

    stack_trace_threshold = sgqlc.types.Field(
        Seconds, graphql_name="stackTraceThreshold"
    )

    transaction_threshold_type = sgqlc.types.Field(
        AgentApplicationSettingsThresholdTypeEnum,
        graphql_name="transactionThresholdType",
    )

    transaction_threshold_value = sgqlc.types.Field(
        Seconds, graphql_name="transactionThresholdValue"
    )


class AgentApplicationSettingsUpdateError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "error_class", "field")
    description = sgqlc.types.Field(String, graphql_name="description")

    error_class = sgqlc.types.Field(
        AgentApplicationSettingsUpdateErrorClass, graphql_name="errorClass"
    )

    field = sgqlc.types.Field(String, graphql_name="field")


class AgentApplicationSettingsUpdateResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "alias",
        "apm_settings",
        "browser_properties",
        "browser_settings",
        "errors",
        "guid",
        "mobile_settings",
    )
    alias = sgqlc.types.Field(String, graphql_name="alias")

    apm_settings = sgqlc.types.Field(
        AgentApplicationSettingsApmBase, graphql_name="apmSettings"
    )

    browser_properties = sgqlc.types.Field(
        AgentApplicationSettingsBrowserProperties, graphql_name="browserProperties"
    )

    browser_settings = sgqlc.types.Field(
        AgentApplicationSettingsBrowserBase, graphql_name="browserSettings"
    )

    errors = sgqlc.types.Field(
        sgqlc.types.list_of(AgentApplicationSettingsUpdateError), graphql_name="errors"
    )

    guid = sgqlc.types.Field(sgqlc.types.non_null(EntityGuid), graphql_name="guid")

    mobile_settings = sgqlc.types.Field(
        AgentApplicationSettingsMobileBase, graphql_name="mobileSettings"
    )


class AgentEnvironmentAccountApplicationLoadedModules(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("application_guids", "details", "loaded_modules")
    application_guids = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EntityGuid))),
        graphql_name="applicationGuids",
    )

    details = sgqlc.types.Field(
        "AgentEnvironmentApplicationInstanceDetails", graphql_name="details"
    )

    loaded_modules = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("AgentEnvironmentApplicationLoadedModule")
        ),
        graphql_name="loadedModules",
    )


class AgentEnvironmentAccountApplicationLoadedModulesResults(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "results")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    results = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(AgentEnvironmentAccountApplicationLoadedModules)
        ),
        graphql_name="results",
    )


class AgentEnvironmentAccountEnvironmentAttributesResults(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "results")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    results = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("AgentEnvironmentApplicationEnvironmentAttributes")
        ),
        graphql_name="results",
    )


class AgentEnvironmentAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("agent_settings_attributes", "environment_attributes", "modules")
    agent_settings_attributes = sgqlc.types.Field(
        AgentEnvironmentAccountEnvironmentAttributesResults,
        graphql_name="agentSettingsAttributes",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        AgentEnvironmentFilter, graphql_name="filter", default=None
                    ),
                ),
            )
        ),
    )

    environment_attributes = sgqlc.types.Field(
        AgentEnvironmentAccountEnvironmentAttributesResults,
        graphql_name="environmentAttributes",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        AgentEnvironmentFilter, graphql_name="filter", default=None
                    ),
                ),
            )
        ),
    )

    modules = sgqlc.types.Field(
        AgentEnvironmentAccountApplicationLoadedModulesResults,
        graphql_name="modules",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        AgentEnvironmentFilter, graphql_name="filter", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `filter` (`AgentEnvironmentFilter`)
    """


class AgentEnvironmentApplicationEnvironmentAttributes(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("application_guids", "attributes", "details")
    application_guids = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EntityGuid))),
        graphql_name="applicationGuids",
    )

    attributes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("AgentEnvironmentAttribute")),
        graphql_name="attributes",
    )

    details = sgqlc.types.Field(
        "AgentEnvironmentApplicationInstanceDetails", graphql_name="details"
    )


class AgentEnvironmentApplicationInstance(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "agent_settings_attributes",
        "details",
        "environment_attributes",
        "modules",
    )
    agent_settings_attributes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("AgentEnvironmentAttribute")),
        graphql_name="agentSettingsAttributes",
        args=sgqlc.types.ArgDict(
            (
                (
                    "filter",
                    sgqlc.types.Arg(
                        AgentEnvironmentFilter, graphql_name="filter", default=None
                    ),
                ),
            )
        ),
    )

    details = sgqlc.types.Field(
        sgqlc.types.non_null("AgentEnvironmentApplicationInstanceDetails"),
        graphql_name="details",
    )

    environment_attributes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("AgentEnvironmentAttribute")),
        graphql_name="environmentAttributes",
        args=sgqlc.types.ArgDict(
            (
                (
                    "filter",
                    sgqlc.types.Arg(
                        AgentEnvironmentFilter, graphql_name="filter", default=None
                    ),
                ),
            )
        ),
    )

    modules = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("AgentEnvironmentApplicationLoadedModule")
        ),
        graphql_name="modules",
        args=sgqlc.types.ArgDict(
            (
                (
                    "filter",
                    sgqlc.types.Arg(
                        AgentEnvironmentFilter, graphql_name="filter", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `filter` (`AgentEnvironmentFilter`)
    """


class AgentEnvironmentApplicationInstanceDetails(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("host", "id", "language", "name")
    host = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="host")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    language = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="language")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class AgentEnvironmentApplicationInstancesResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("application_instances", "next_cursor")
    application_instances = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(AgentEnvironmentApplicationInstance)),
        graphql_name="applicationInstances",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")


class AgentEnvironmentApplicationLoadedModule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attributes", "name", "version")
    attributes = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of("AgentEnvironmentLoadedModuleAttribute")
        ),
        graphql_name="attributes",
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(String, graphql_name="version")


class AgentEnvironmentAttribute(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attribute", "value")
    attribute = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="attribute"
    )

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class AgentEnvironmentLoadedModuleAttribute(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class AgentFeatures(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("min_version", "name")
    min_version = sgqlc.types.Field(String, graphql_name="minVersion")

    name = sgqlc.types.Field(String, graphql_name="name")


class AgentRelease(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "bugs",
        "date",
        "download_link",
        "eol_date",
        "features",
        "security",
        "slug",
        "version",
    )
    bugs = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="bugs")

    date = sgqlc.types.Field(Date, graphql_name="date")

    download_link = sgqlc.types.Field(String, graphql_name="downloadLink")

    eol_date = sgqlc.types.Field(Date, graphql_name="eolDate")

    features = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="features")

    security = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="security")

    slug = sgqlc.types.Field(String, graphql_name="slug")

    version = sgqlc.types.Field(String, graphql_name="version")


class AiDecisionsAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("decision", "decisions")
    decision = sgqlc.types.Field(
        "AiDecisionsDecision",
        graphql_name="decision",
        args=sgqlc.types.ArgDict(
            (
                (
                    "decision_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="decisionId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    decisions = sgqlc.types.Field(
        sgqlc.types.non_null("AiDecisionsDecisionListing"),
        graphql_name="decisions",
        args=sgqlc.types.ArgDict(
            (
                ("after", sgqlc.types.Arg(String, graphql_name="after", default=None)),
                (
                    "before",
                    sgqlc.types.Arg(String, graphql_name="before", default=None),
                ),
                (
                    "decision_states",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(
                            sgqlc.types.non_null(AiDecisionsDecisionState)
                        ),
                        graphql_name="decisionStates",
                        default=None,
                    ),
                ),
                (
                    "decision_types",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(
                            sgqlc.types.non_null(AiDecisionsDecisionType)
                        ),
                        graphql_name="decisionTypes",
                        default=None,
                    ),
                ),
                (
                    "page_size",
                    sgqlc.types.Arg(Int, graphql_name="pageSize", default=None),
                ),
                (
                    "sort_method",
                    sgqlc.types.Arg(
                        AiDecisionsDecisionSortMethod,
                        graphql_name="sortMethod",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `after` (`String`)
    * `before` (`String`)
    * `decision_states` (`[AiDecisionsDecisionState!]`)
    * `decision_types` (`[AiDecisionsDecisionType!]`)
    * `page_size` (`Int`)
    * `sort_method` (`AiDecisionsDecisionSortMethod`)
    """


class AiDecisionsAnnotationEntry(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("key", "value")
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class AiDecisionsApplicableIncidentSearch(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "completed_at",
        "created_at",
        "error_message",
        "id",
        "incidents_scanned",
        "results",
        "updated_at",
    )
    completed_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="completedAt")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    error_message = sgqlc.types.Field(String, graphql_name="errorMessage")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    incidents_scanned = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="incidentsScanned"
    )

    results = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiDecisionsSelectorExamples"))
        ),
        graphql_name="results",
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="updatedAt"
    )


class AiDecisionsDecision(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "annotations",
        "correlation_window_length",
        "created_at",
        "creator",
        "decision_expression",
        "decision_type",
        "description",
        "id",
        "metadata",
        "min_correlation_threshold",
        "name",
        "override_configuration",
        "source",
        "state",
        "updated_at",
    )
    annotations = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiDecisionsAnnotationEntry))
        ),
        graphql_name="annotations",
    )

    correlation_window_length = sgqlc.types.Field(
        Milliseconds, graphql_name="correlationWindowLength"
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    creator = sgqlc.types.Field("UserReference", graphql_name="creator")

    decision_expression = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRuleExpression),
        graphql_name="decisionExpression",
    )

    decision_type = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsDecisionType), graphql_name="decisionType"
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    metadata = sgqlc.types.Field(
        sgqlc.types.non_null("AiDecisionsRuleMetadata"), graphql_name="metadata"
    )

    min_correlation_threshold = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="minCorrelationThreshold"
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    override_configuration = sgqlc.types.Field(
        "AiDecisionsOverrideConfiguration", graphql_name="overrideConfiguration"
    )

    source = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRuleSource), graphql_name="source"
    )

    state = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsDecisionState), graphql_name="state"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="updatedAt"
    )


class AiDecisionsDecisionListing(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "decisions", "next_cursor", "prev_cursor")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")

    decisions = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiDecisionsDecision))
        ),
        graphql_name="decisions",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    prev_cursor = sgqlc.types.Field(String, graphql_name="prevCursor")


class AiDecisionsMergeFeedback(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "child_issue_id",
        "opinion",
        "parent_issue_id",
        "rule_id",
        "user_id",
    )
    child_issue_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="childIssueId"
    )

    opinion = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsOpinion), graphql_name="opinion"
    )

    parent_issue_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="parentIssueId"
    )

    rule_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="ruleId")

    user_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="userId")


class AiDecisionsOperationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("result",)
    result = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsResultType), graphql_name="result"
    )


class AiDecisionsOpinionEntry(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "opinion")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")

    opinion = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsOpinion), graphql_name="opinion"
    )


class AiDecisionsOverrideConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "priority", "title")
    description = sgqlc.types.Field(String, graphql_name="description")

    priority = sgqlc.types.Field(AiDecisionsIssuePriority, graphql_name="priority")

    title = sgqlc.types.Field(String, graphql_name="title")


class AiDecisionsRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "annotations",
        "correlation_window_length",
        "created_at",
        "creator",
        "description",
        "id",
        "metadata",
        "min_correlation_threshold",
        "name",
        "override_configuration",
        "rule_expression",
        "rule_type",
        "source",
        "state",
        "updated_at",
    )
    annotations = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiDecisionsAnnotationEntry))
        ),
        graphql_name="annotations",
    )

    correlation_window_length = sgqlc.types.Field(
        Milliseconds, graphql_name="correlationWindowLength"
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    creator = sgqlc.types.Field("UserReference", graphql_name="creator")

    description = sgqlc.types.Field(String, graphql_name="description")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    metadata = sgqlc.types.Field(
        sgqlc.types.non_null("AiDecisionsRuleMetadata"), graphql_name="metadata"
    )

    min_correlation_threshold = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="minCorrelationThreshold"
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    override_configuration = sgqlc.types.Field(
        AiDecisionsOverrideConfiguration, graphql_name="overrideConfiguration"
    )

    rule_expression = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRuleExpression), graphql_name="ruleExpression"
    )

    rule_type = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRuleType), graphql_name="ruleType"
    )

    source = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRuleSource), graphql_name="source"
    )

    state = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRuleState), graphql_name="state"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="updatedAt"
    )


class AiDecisionsRuleMetadata(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("merge_opinion_count",)
    merge_opinion_count = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiDecisionsOpinionEntry))
        ),
        graphql_name="mergeOpinionCount",
    )


class AiDecisionsSelectorApplicability(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "select")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")

    select = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsIncidentSelect), graphql_name="select"
    )


class AiDecisionsSelectorExamples(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("incidents", "select")
    incidents = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))),
        graphql_name="incidents",
    )

    select = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsIncidentSelect), graphql_name="select"
    )


class AiDecisionsSimulation(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "candidate_incidents",
        "completed_at",
        "created_at",
        "error_message",
        "id",
        "incidents_applicable",
        "incidents_correlated",
        "incidents_ingested",
        "incidents_processed",
        "progress",
        "updated_at",
    )
    candidate_incidents = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID)))
            )
        ),
        graphql_name="candidateIncidents",
    )

    completed_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="completedAt")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    error_message = sgqlc.types.Field(String, graphql_name="errorMessage")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    incidents_applicable = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiDecisionsSelectorApplicability))
        ),
        graphql_name="incidentsApplicable",
    )

    incidents_correlated = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="incidentsCorrelated"
    )

    incidents_ingested = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="incidentsIngested"
    )

    incidents_processed = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="incidentsProcessed"
    )

    progress = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name="progress")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="updatedAt"
    )


class AiDecisionsSuggestion(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "correlation_window_length",
        "created_at",
        "description",
        "hash",
        "id",
        "min_correlation_threshold",
        "name",
        "override_configuration",
        "rule_expression",
        "state",
        "suggester",
        "support",
    )
    correlation_window_length = sgqlc.types.Field(
        Milliseconds, graphql_name="correlationWindowLength"
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    hash = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="hash")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    min_correlation_threshold = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="minCorrelationThreshold"
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    override_configuration = sgqlc.types.Field(
        AiDecisionsOverrideConfiguration, graphql_name="overrideConfiguration"
    )

    rule_expression = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRuleExpression), graphql_name="ruleExpression"
    )

    state = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsSuggestionState), graphql_name="state"
    )

    suggester = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="suggester"
    )

    support = sgqlc.types.Field(String, graphql_name="support")


class AiIssuesAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "config_by_environment",
        "incidents",
        "incidents_events",
        "issues",
        "issues_events",
    )
    config_by_environment = sgqlc.types.Field(
        "AiIssuesConfigurationByEnvironment", graphql_name="configByEnvironment"
    )

    incidents = sgqlc.types.Field(
        "AiIssuesIncidentData",
        graphql_name="incidents",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        AiIssuesFilterIncidents, graphql_name="filter", default=None
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )

    incidents_events = sgqlc.types.Field(
        "AiIssuesIncidentData",
        graphql_name="incidentsEvents",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        AiIssuesFilterIncidentsEvents,
                        graphql_name="filter",
                        default=None,
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )

    issues = sgqlc.types.Field(
        "AiIssuesIssueData",
        graphql_name="issues",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        AiIssuesFilterIssues, graphql_name="filter", default=None
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )

    issues_events = sgqlc.types.Field(
        "AiIssuesIssueData",
        graphql_name="issuesEvents",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        AiIssuesFilterIssuesEvents, graphql_name="filter", default=None
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `filter` (`AiIssuesFilterIssuesEvents`)
    * `time_window` (`TimeWindowInput`)
    """


class AiIssuesConfigurationByEnvironment(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("config",)
    config = sgqlc.types.Field(
        "AiIssuesEnvironmentConfiguration", graphql_name="config"
    )


class AiIssuesConfigurationOverrideResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("config", "error")
    config = sgqlc.types.Field(
        "AiIssuesEnvironmentConfiguration", graphql_name="config"
    )

    error = sgqlc.types.Field(String, graphql_name="error")


class AiIssuesEnvironmentConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "flapping_interval",
        "grace_period",
        "inactive_period",
        "incident_timeout",
        "issue_ttl",
        "max_issue_size",
    )
    flapping_interval = sgqlc.types.Field(Seconds, graphql_name="flappingInterval")

    grace_period = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("AiIssuesGracePeriodConfig")),
        graphql_name="gracePeriod",
    )

    inactive_period = sgqlc.types.Field(Seconds, graphql_name="inactivePeriod")

    incident_timeout = sgqlc.types.Field(Seconds, graphql_name="incidentTimeout")

    issue_ttl = sgqlc.types.Field(Seconds, graphql_name="issueTtl")

    max_issue_size = sgqlc.types.Field(Int, graphql_name="maxIssueSize")


class AiIssuesGracePeriodConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("period", "priority")
    period = sgqlc.types.Field(sgqlc.types.non_null(Seconds), graphql_name="period")

    priority = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesPriority), graphql_name="priority"
    )


class AiIssuesIncidentData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("incidents", "next_cursor")
    incidents = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiIssuesIIncident))
        ),
        graphql_name="incidents",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")


class AiIssuesIncidentUserActionResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "error", "incident_id")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    error = sgqlc.types.Field(String, graphql_name="error")

    incident_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="incidentId")


class AiIssuesIssue(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_ids",
        "acknowledged_at",
        "acknowledged_by",
        "activated_at",
        "closed_at",
        "closed_by",
        "condition_family_id",
        "condition_name",
        "condition_product",
        "correlation_rule_descriptions",
        "correlation_rule_ids",
        "correlation_rule_names",
        "created_at",
        "data_ml_modules",
        "deep_link_url",
        "description",
        "entity_guids",
        "entity_names",
        "entity_types",
        "environment_id",
        "event_type",
        "incident_ids",
        "is_correlated",
        "is_idle",
        "issue_id",
        "merge_reason",
        "muting_state",
        "origins",
        "parent_merge_id",
        "policy_ids",
        "policy_name",
        "priority",
        "sources",
        "state",
        "title",
        "total_incidents",
        "un_acknowledged_at",
        "un_acknowledged_by",
        "updated_at",
        "wildcard",
    )
    account_ids = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int))),
        graphql_name="accountIds",
    )

    acknowledged_at = sgqlc.types.Field(
        EpochMilliseconds, graphql_name="acknowledgedAt"
    )

    acknowledged_by = sgqlc.types.Field(String, graphql_name="acknowledgedBy")

    activated_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="activatedAt")

    closed_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="closedAt")

    closed_by = sgqlc.types.Field(String, graphql_name="closedBy")

    condition_family_id = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="conditionFamilyId"
    )

    condition_name = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="conditionName"
    )

    condition_product = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="conditionProduct",
    )

    correlation_rule_descriptions = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="correlationRuleDescriptions",
    )

    correlation_rule_ids = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(Int)),
        graphql_name="correlationRuleIds",
    )

    correlation_rule_names = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="correlationRuleNames",
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    data_ml_modules = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("AiIssuesKeyValues")),
        graphql_name="dataMlModules",
    )

    deep_link_url = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="deepLinkUrl"
    )

    description = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="description",
    )

    entity_guids = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(EntityGuid)),
        graphql_name="entityGuids",
    )

    entity_names = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="entityNames"
    )

    entity_types = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="entityTypes"
    )

    environment_id = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="environmentId"
    )

    event_type = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="eventType"
    )

    incident_ids = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="incidentIds"
    )

    is_correlated = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="isCorrelated"
    )

    is_idle = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="isIdle")

    issue_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="issueId")

    merge_reason = sgqlc.types.Field(String, graphql_name="mergeReason")

    muting_state = sgqlc.types.Field(
        AiIssuesIssueMutingState, graphql_name="mutingState"
    )

    origins = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="origins",
    )

    parent_merge_id = sgqlc.types.Field(String, graphql_name="parentMergeId")

    policy_ids = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="policyIds"
    )

    policy_name = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="policyName"
    )

    priority = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesPriority), graphql_name="priority"
    )

    sources = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="sources",
    )

    state = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesIssueState), graphql_name="state"
    )

    title = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="title",
    )

    total_incidents = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalIncidents"
    )

    un_acknowledged_at = sgqlc.types.Field(
        EpochMilliseconds, graphql_name="unAcknowledgedAt"
    )

    un_acknowledged_by = sgqlc.types.Field(String, graphql_name="unAcknowledgedBy")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="updatedAt"
    )

    wildcard = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="wildcard"
    )


class AiIssuesIssueData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("issues", "next_cursor")
    issues = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(AiIssuesIssue))),
        graphql_name="issues",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")


class AiIssuesIssueUserActionResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error", "result")
    error = sgqlc.types.Field(String, graphql_name="error")

    result = sgqlc.types.Field("AiIssuesIssueUserActionResult", graphql_name="result")


class AiIssuesIssueUserActionResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "action", "issue_id")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    action = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesIssueUserAction), graphql_name="action"
    )

    issue_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="issueId")


class AiIssuesKeyValue(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("key", "value")
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class AiIssuesKeyValues(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("key", "value")
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    value = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="value",
    )


class AiNotificationsAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "channel_schema",
        "channel_suggestions",
        "channels",
        "destination_suggestions",
        "destinations",
        "o_auth_url",
        "variables",
    )
    channel_schema = sgqlc.types.Field(
        "AiNotificationsChannelSchemaResult",
        graphql_name="channelSchema",
        args=sgqlc.types.ArgDict(
            (
                (
                    "channel_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiNotificationsChannelType),
                        graphql_name="channelType",
                        default=None,
                    ),
                ),
                (
                    "constraints",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(
                            sgqlc.types.non_null(AiNotificationsConstraint)
                        ),
                        graphql_name="constraints",
                        default=None,
                    ),
                ),
                (
                    "destination_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="destinationId",
                        default=None,
                    ),
                ),
                (
                    "product",
                    sgqlc.types.Arg(
                        AiNotificationsProduct, graphql_name="product", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `channel_type` (`AiNotificationsChannelType!`)
    * `constraints` (`[AiNotificationsConstraint!]`)
    * `destination_id` (`ID!`)
    * `product` (`AiNotificationsProduct`)
    """

    channel_suggestions = sgqlc.types.Field(
        "AiNotificationsSuggestionsResponse",
        graphql_name="channelSuggestions",
        args=sgqlc.types.ArgDict(
            (
                (
                    "channel_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiNotificationsChannelType),
                        graphql_name="channelType",
                        default=None,
                    ),
                ),
                (
                    "constraints",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(
                            sgqlc.types.non_null(AiNotificationsConstraint)
                        ),
                        graphql_name="constraints",
                        default=None,
                    ),
                ),
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "destination_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="destinationId",
                        default=None,
                    ),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        AiNotificationsSuggestionFilter,
                        graphql_name="filter",
                        default=None,
                    ),
                ),
                (
                    "key",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="key", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `channel_type` (`AiNotificationsChannelType!`)
    * `constraints` (`[AiNotificationsConstraint!]`)
    * `cursor` (`String`)
    * `destination_id` (`ID!`)
    * `filter` (`AiNotificationsSuggestionFilter`)
    * `key` (`String!`)
    """

    channels = sgqlc.types.Field(
        "AiNotificationsChannelsResponse",
        graphql_name="channels",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filters",
                    sgqlc.types.Arg(
                        AiNotificationsChannelFilter,
                        graphql_name="filters",
                        default=None,
                    ),
                ),
                (
                    "sorter",
                    sgqlc.types.Arg(
                        AiNotificationsChannelSorter,
                        graphql_name="sorter",
                        default=None,
                    ),
                ),
            )
        ),
    )

    destination_suggestions = sgqlc.types.Field(
        "AiNotificationsSuggestionsResponse",
        graphql_name="destinationSuggestions",
        args=sgqlc.types.ArgDict(
            (
                (
                    "constraints",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(
                            sgqlc.types.non_null(AiNotificationsConstraint)
                        ),
                        graphql_name="constraints",
                        default=None,
                    ),
                ),
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "destination_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiNotificationsDestinationType),
                        graphql_name="destinationType",
                        default=None,
                    ),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        AiNotificationsSuggestionFilter,
                        graphql_name="filter",
                        default=None,
                    ),
                ),
                (
                    "key",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="key", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `constraints` (`[AiNotificationsConstraint!]`)
    * `cursor` (`String`)
    * `destination_type` (`AiNotificationsDestinationType!`)
    * `filter` (`AiNotificationsSuggestionFilter`)
    * `key` (`String!`)
    """

    destinations = sgqlc.types.Field(
        "AiNotificationsDestinationsResponse",
        graphql_name="destinations",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filters",
                    sgqlc.types.Arg(
                        AiNotificationsDestinationFilter,
                        graphql_name="filters",
                        default=None,
                    ),
                ),
                (
                    "sorter",
                    sgqlc.types.Arg(
                        AiNotificationsDestinationSorter,
                        graphql_name="sorter",
                        default=None,
                    ),
                ),
            )
        ),
    )

    o_auth_url = sgqlc.types.Field(
        "AiNotificationsOAuthUrlResponse",
        graphql_name="oAuthUrl",
        args=sgqlc.types.ArgDict(
            (
                (
                    "redirect_url",
                    sgqlc.types.Arg(String, graphql_name="redirectUrl", default=None),
                ),
                (
                    "type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiNotificationsDestinationType),
                        graphql_name="type",
                        default=None,
                    ),
                ),
            )
        ),
    )

    variables = sgqlc.types.Field(
        "AiNotificationsVariableResult",
        graphql_name="variables",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filters",
                    sgqlc.types.Arg(
                        AiNotificationsVariableFilter,
                        graphql_name="filters",
                        default=None,
                    ),
                ),
                (
                    "sorter",
                    sgqlc.types.Arg(
                        AiNotificationsVariableSorter,
                        graphql_name="sorter",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `filters` (`AiNotificationsVariableFilter`)
    * `sorter` (`AiNotificationsVariableSorter`)
    """


class AiNotificationsBasicAuth(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("auth_type", "user")
    auth_type = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsAuthType), graphql_name="authType"
    )

    user = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="user")


class AiNotificationsChannel(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "active",
        "created_at",
        "destination_id",
        "id",
        "name",
        "product",
        "properties",
        "status",
        "type",
        "updated_at",
        "updated_by",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="active")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    destination_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="destinationId"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    product = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsProduct), graphql_name="product"
    )

    properties = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiNotificationsProperty"))
        ),
        graphql_name="properties",
    )

    status = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsChannelStatus), graphql_name="status"
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsChannelType), graphql_name="type"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )

    updated_by = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="updatedBy")


class AiNotificationsChannelResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("channel", "error")
    channel = sgqlc.types.Field(AiNotificationsChannel, graphql_name="channel")

    error = sgqlc.types.Field("AiNotificationsError", graphql_name="error")


class AiNotificationsChannelSchemaResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error", "result", "schema")
    error = sgqlc.types.Field("AiNotificationsError", graphql_name="error")

    result = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsResult), graphql_name="result"
    )

    schema = sgqlc.types.Field("AiNotificationsSchema", graphql_name="schema")


class AiNotificationsChannelTestResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("details", "error", "evidence", "result")
    details = sgqlc.types.Field(String, graphql_name="details")

    error = sgqlc.types.Field("AiNotificationsError", graphql_name="error")

    evidence = sgqlc.types.Field(String, graphql_name="evidence")

    result = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsResult), graphql_name="result"
    )


class AiNotificationsChannelsResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entities", "error", "next_cursor", "total_count")
    entities = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiNotificationsChannel))
        ),
        graphql_name="entities",
    )

    error = sgqlc.types.Field("AiNotificationsResponseError", graphql_name="error")

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AiNotificationsConstraintError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("dependencies", "name")
    dependencies = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="dependencies",
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class AiNotificationsConstraintsError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("constraints",)
    constraints = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiNotificationsConstraintError))
        ),
        graphql_name="constraints",
    )


class AiNotificationsDataValidationError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("details", "fields")
    details = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="details")

    fields = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiNotificationsFieldError"))
        ),
        graphql_name="fields",
    )


class AiNotificationsDeleteResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error", "ids")
    error = sgqlc.types.Field("AiNotificationsResponseError", graphql_name="error")

    ids = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name="ids"
    )


class AiNotificationsDestination(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "active",
        "auth",
        "created_at",
        "id",
        "is_user_authenticated",
        "last_sent",
        "name",
        "properties",
        "status",
        "type",
        "updated_at",
        "updated_by",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="active")

    auth = sgqlc.types.Field("AiNotificationsAuth", graphql_name="auth")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    is_user_authenticated = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="isUserAuthenticated"
    )

    last_sent = sgqlc.types.Field(DateTime, graphql_name="lastSent")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    properties = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiNotificationsProperty"))
        ),
        graphql_name="properties",
    )

    status = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsDestinationStatus), graphql_name="status"
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsDestinationType), graphql_name="type"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )

    updated_by = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="updatedBy")


class AiNotificationsDestinationResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("destination", "error")
    destination = sgqlc.types.Field(
        AiNotificationsDestination, graphql_name="destination"
    )

    error = sgqlc.types.Field("AiNotificationsError", graphql_name="error")


class AiNotificationsDestinationTestResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("details", "error", "result")
    details = sgqlc.types.Field(String, graphql_name="details")

    error = sgqlc.types.Field("AiNotificationsError", graphql_name="error")

    result = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsResult), graphql_name="result"
    )


class AiNotificationsDestinationsResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entities", "error", "next_cursor", "total_count")
    entities = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiNotificationsDestination))
        ),
        graphql_name="entities",
    )

    error = sgqlc.types.Field("AiNotificationsResponseError", graphql_name="error")

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AiNotificationsFieldError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("field", "message")
    field = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="field")

    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")


class AiNotificationsOAuth2Auth(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "access_token_url",
        "auth_type",
        "authorization_url",
        "client_id",
        "prefix",
        "refresh_interval",
        "refreshable",
        "scope",
    )
    access_token_url = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="accessTokenUrl"
    )

    auth_type = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsAuthType), graphql_name="authType"
    )

    authorization_url = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="authorizationUrl"
    )

    client_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="clientId")

    prefix = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="prefix")

    refresh_interval = sgqlc.types.Field(Int, graphql_name="refreshInterval")

    refreshable = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="refreshable"
    )

    scope = sgqlc.types.Field(String, graphql_name="scope")


class AiNotificationsOAuthUrlResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error", "transaction_id", "url")
    error = sgqlc.types.Field("AiNotificationsResponseError", graphql_name="error")

    transaction_id = sgqlc.types.Field(ID, graphql_name="transactionId")

    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class AiNotificationsProperty(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("display_value", "key", "label", "value")
    display_value = sgqlc.types.Field(String, graphql_name="displayValue")

    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    label = sgqlc.types.Field(String, graphql_name="label")

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class AiNotificationsResponseError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "details", "type")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    details = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="details")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsErrorType), graphql_name="type"
    )


class AiNotificationsSchema(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("fields",)
    fields = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiNotificationsSchemaField"))
        ),
        graphql_name="fields",
    )


class AiNotificationsSchemaField(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("component", "key", "label", "mandatory")
    component = sgqlc.types.Field(
        sgqlc.types.non_null("AiNotificationsUiComponent"), graphql_name="component"
    )

    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="label")

    mandatory = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="mandatory"
    )


class AiNotificationsSelectComponentOptions(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "creatable",
        "dependent_on",
        "filtered_by",
        "label",
        "multiple",
        "searchable",
        "suggestions",
    )
    creatable = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="creatable"
    )

    dependent_on = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="dependentOn",
    )

    filtered_by = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="filteredBy",
    )

    label = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="label")

    multiple = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="multiple")

    searchable = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="searchable"
    )

    suggestions = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiNotificationsSuggestion"))
        ),
        graphql_name="suggestions",
    )


class AiNotificationsSuggestion(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("display_value", "icon", "value")
    display_value = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="displayValue"
    )

    icon = sgqlc.types.Field(String, graphql_name="icon")

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class AiNotificationsSuggestionError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ()


class AiNotificationsSuggestionsResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entities", "error", "next_cursor", "result", "total_count")
    entities = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiNotificationsSuggestion))
        ),
        graphql_name="entities",
    )

    error = sgqlc.types.Field("AiNotificationsError", graphql_name="error")

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    result = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsResult), graphql_name="result"
    )

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AiNotificationsTokenAuth(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("auth_type", "prefix")
    auth_type = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsAuthType), graphql_name="authType"
    )

    prefix = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="prefix")


class AiNotificationsUiComponent(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "allow_template_variables",
        "data_validation",
        "default_value",
        "select_options",
        "type",
        "visible_by_default",
    )
    allow_template_variables = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="allowTemplateVariables"
    )

    data_validation = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsUiComponentValidation),
        graphql_name="dataValidation",
    )

    default_value = sgqlc.types.Field(
        AiNotificationsSuggestion, graphql_name="defaultValue"
    )

    select_options = sgqlc.types.Field(
        AiNotificationsSelectComponentOptions, graphql_name="selectOptions"
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsUiComponentType), graphql_name="type"
    )

    visible_by_default = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="visibleByDefault"
    )


class AiNotificationsVariable(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "active",
        "category",
        "created_at",
        "description",
        "example",
        "id",
        "key",
        "label",
        "name",
        "product",
        "type",
        "updated_at",
        "updated_by",
    )
    active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="active")

    category = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsVariableCategory), graphql_name="category"
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    example = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="example")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    label = sgqlc.types.Field(String, graphql_name="label")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    product = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsProduct), graphql_name="product"
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsVariableType), graphql_name="type"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )

    updated_by = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="updatedBy")


class AiNotificationsVariableResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entities", "next_cursor", "total_count")
    entities = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiNotificationsVariable))
        ),
        graphql_name="entities",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AiTopologyAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("edges", "graph", "vertices")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null("AiTopologyEdgeListing"),
        graphql_name="edges",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "edge_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="edgeIds",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `edge_ids` (`[ID!]`)
    """

    graph = sgqlc.types.Field(
        sgqlc.types.non_null("AiTopologyGraph"), graphql_name="graph"
    )

    vertices = sgqlc.types.Field(
        sgqlc.types.non_null("AiTopologyVertexListing"),
        graphql_name="vertices",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "vertex_classes",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(
                            sgqlc.types.non_null(AiTopologyVertexClass)
                        ),
                        graphql_name="vertexClasses",
                        default=None,
                    ),
                ),
                (
                    "vertex_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="vertexIds",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `vertex_classes` (`[AiTopologyVertexClass!]`)
    * `vertex_ids` (`[ID!]`)
    """


class AiTopologyCollectorOperationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("result",)
    result = sgqlc.types.Field(
        sgqlc.types.non_null(AiTopologyCollectorResultType), graphql_name="result"
    )


class AiTopologyDefiningAttribute(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("key", "value")
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class AiTopologyEdge(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "directed",
        "from_vertex_id",
        "from_vertex_name",
        "id",
        "to_vertex_id",
        "to_vertex_name",
        "updated_at",
    )
    directed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="directed")

    from_vertex_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="fromVertexId"
    )

    from_vertex_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="fromVertexName"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    to_vertex_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="toVertexId"
    )

    to_vertex_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="toVertexName"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="updatedAt"
    )


class AiTopologyEdgeListing(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "cursor", "edges")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")

    cursor = sgqlc.types.Field(String, graphql_name="cursor")

    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(AiTopologyEdge))),
        graphql_name="edges",
    )


class AiTopologyGraph(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("edges", "vertices")
    edges = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(AiTopologyEdge))),
        graphql_name="edges",
    )

    vertices = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiTopologyVertex"))
        ),
        graphql_name="vertices",
    )


class AiTopologyVertex(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "defining_attributes",
        "id",
        "name",
        "updated_at",
        "vertex_class",
    )
    defining_attributes = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiTopologyDefiningAttribute))
        ),
        graphql_name="definingAttributes",
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="updatedAt"
    )

    vertex_class = sgqlc.types.Field(
        sgqlc.types.non_null(AiTopologyVertexClass), graphql_name="vertexClass"
    )


class AiTopologyVertexListing(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "cursor", "vertices")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")

    cursor = sgqlc.types.Field(String, graphql_name="cursor")

    vertices = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiTopologyVertex))
        ),
        graphql_name="vertices",
    )


class AiWorkflowsAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("workflows",)
    workflows = sgqlc.types.Field(
        "AiWorkflowsWorkflows",
        graphql_name="workflows",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filters",
                    sgqlc.types.Arg(
                        AiWorkflowsFilters, graphql_name="filters", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `filters` (`AiWorkflowsFilters`)
    """


class AiWorkflowsCreateWorkflowResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "workflow")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiWorkflowsCreateResponseError"))
        ),
        graphql_name="errors",
    )

    workflow = sgqlc.types.Field("AiWorkflowsWorkflow", graphql_name="workflow")


class AiWorkflowsDeleteWorkflowResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "id")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiWorkflowsDeleteResponseError"))
        ),
        graphql_name="errors",
    )

    id = sgqlc.types.Field(ID, graphql_name="id")


class AiWorkflowsDestinationConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("channel_id", "name", "notification_triggers", "type")
    channel_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="channelId")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    notification_triggers = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(AiWorkflowsNotificationTrigger)),
        graphql_name="notificationTriggers",
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsDestinationType), graphql_name="type"
    )


class AiWorkflowsEnrichment(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "configurations",
        "created_at",
        "id",
        "name",
        "type",
        "updated_at",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    configurations = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiWorkflowsConfiguration"))
        ),
        graphql_name="configurations",
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsEnrichmentType), graphql_name="type"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )


class AiWorkflowsFilter(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "id", "name", "predicates", "type")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    predicates = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiWorkflowsPredicate"))
        ),
        graphql_name="predicates",
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsFilterType), graphql_name="type"
    )


class AiWorkflowsNrqlConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("query",)
    query = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="query")


class AiWorkflowsPredicate(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attribute", "operator", "values")
    attribute = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="attribute"
    )

    operator = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsOperator), graphql_name="operator"
    )

    values = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="values",
    )


class AiWorkflowsTestNotificationResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("channel_id", "evidence", "status")
    channel_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="channelId")

    evidence = sgqlc.types.Field(String, graphql_name="evidence")

    status = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsTestNotificationResponseStatus),
        graphql_name="status",
    )


class AiWorkflowsTestWorkflowResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "notification_responses", "status")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("AiWorkflowsTestResponseError")),
        graphql_name="errors",
    )

    notification_responses = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(AiWorkflowsTestNotificationResponse)),
        graphql_name="notificationResponses",
    )

    status = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsTestResponseStatus), graphql_name="status"
    )


class AiWorkflowsUpdateWorkflowResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "workflow")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AiWorkflowsUpdateResponseError"))
        ),
        graphql_name="errors",
    )

    workflow = sgqlc.types.Field("AiWorkflowsWorkflow", graphql_name="workflow")


class AiWorkflowsWorkflow(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "created_at",
        "destination_configurations",
        "destinations_enabled",
        "enrichments",
        "enrichments_enabled",
        "guid",
        "id",
        "issues_filter",
        "last_run",
        "muting_rules_handling",
        "name",
        "updated_at",
        "workflow_enabled",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    destination_configurations = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(AiWorkflowsDestinationConfiguration)
            )
        ),
        graphql_name="destinationConfigurations",
    )

    destinations_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="destinationsEnabled"
    )

    enrichments = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiWorkflowsEnrichment))
        ),
        graphql_name="enrichments",
    )

    enrichments_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="enrichmentsEnabled"
    )

    guid = sgqlc.types.Field(sgqlc.types.non_null(EntityGuid), graphql_name="guid")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    issues_filter = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsFilter), graphql_name="issuesFilter"
    )

    last_run = sgqlc.types.Field(DateTime, graphql_name="lastRun")

    muting_rules_handling = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsMutingRulesHandling),
        graphql_name="mutingRulesHandling",
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )

    workflow_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="workflowEnabled"
    )


class AiWorkflowsWorkflows(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entities", "next_cursor", "total_count")
    entities = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AiWorkflowsWorkflow))
        ),
        graphql_name="entities",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AlertsAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "muting_rule",
        "muting_rules",
        "notification_channel",
        "notification_channels",
        "nrql_condition",
        "nrql_conditions_search",
        "policies_search",
        "policy",
    )
    muting_rule = sgqlc.types.Field(
        "AlertsMutingRule",
        graphql_name="mutingRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    muting_rules = sgqlc.types.Field(
        sgqlc.types.list_of("AlertsMutingRule"), graphql_name="mutingRules"
    )

    notification_channel = sgqlc.types.Field(
        AlertsNotificationChannel,
        graphql_name="notificationChannel",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    notification_channels = sgqlc.types.Field(
        "AlertsNotificationChannelsResultSet",
        graphql_name="notificationChannels",
        args=sgqlc.types.ArgDict(
            (("cursor", sgqlc.types.Arg(String, graphql_name="cursor", default=None)),)
        ),
    )

    nrql_condition = sgqlc.types.Field(
        AlertsNrqlCondition,
        graphql_name="nrqlCondition",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    nrql_conditions_search = sgqlc.types.Field(
        "AlertsNrqlConditionsSearchResultSet",
        graphql_name="nrqlConditionsSearch",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "search_criteria",
                    sgqlc.types.Arg(
                        AlertsNrqlConditionsSearchCriteriaInput,
                        graphql_name="searchCriteria",
                        default=None,
                    ),
                ),
            )
        ),
    )

    policies_search = sgqlc.types.Field(
        "AlertsPoliciesSearchResultSet",
        graphql_name="policiesSearch",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "search_criteria",
                    sgqlc.types.Arg(
                        AlertsPoliciesSearchCriteriaInput,
                        graphql_name="searchCriteria",
                        default=None,
                    ),
                ),
            )
        ),
    )

    policy = sgqlc.types.Field(
        "AlertsPolicy",
        graphql_name="policy",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID!`)
    """


class AlertsCampfireNotificationChannelConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ()


class AlertsConditionDeleteResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class AlertsEmailNotificationChannelConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("emails", "include_json")
    emails = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="emails",
    )

    include_json = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="includeJson"
    )


class AlertsHipChatNotificationChannelConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ()


class AlertsMutingRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "condition",
        "created_at",
        "created_by_user",
        "description",
        "enabled",
        "id",
        "name",
        "schedule",
        "status",
        "updated_at",
        "updated_by_user",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    condition = sgqlc.types.Field(
        sgqlc.types.non_null("AlertsMutingRuleConditionGroup"), graphql_name="condition"
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    created_by_user = sgqlc.types.Field("UserReference", graphql_name="createdByUser")

    description = sgqlc.types.Field(String, graphql_name="description")

    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    schedule = sgqlc.types.Field("AlertsMutingRuleSchedule", graphql_name="schedule")

    status = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsMutingRuleStatus), graphql_name="status"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )

    updated_by_user = sgqlc.types.Field("UserReference", graphql_name="updatedByUser")


class AlertsMutingRuleCondition(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attribute", "operator", "values")
    attribute = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="attribute"
    )

    operator = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsMutingRuleConditionOperator), graphql_name="operator"
    )

    values = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name="values"
    )


class AlertsMutingRuleConditionGroup(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("conditions", "operator")
    conditions = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AlertsMutingRuleCondition))
        ),
        graphql_name="conditions",
    )

    operator = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsMutingRuleConditionGroupOperator),
        graphql_name="operator",
    )


class AlertsMutingRuleDeleteResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class AlertsMutingRuleSchedule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "end_repeat",
        "end_time",
        "next_end_time",
        "next_start_time",
        "repeat",
        "repeat_count",
        "start_time",
        "time_zone",
        "weekly_repeat_days",
    )
    end_repeat = sgqlc.types.Field(DateTime, graphql_name="endRepeat")

    end_time = sgqlc.types.Field(DateTime, graphql_name="endTime")

    next_end_time = sgqlc.types.Field(DateTime, graphql_name="nextEndTime")

    next_start_time = sgqlc.types.Field(DateTime, graphql_name="nextStartTime")

    repeat = sgqlc.types.Field(AlertsMutingRuleScheduleRepeat, graphql_name="repeat")

    repeat_count = sgqlc.types.Field(Int, graphql_name="repeatCount")

    start_time = sgqlc.types.Field(DateTime, graphql_name="startTime")

    time_zone = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="timeZone")

    weekly_repeat_days = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(AlertsDayOfWeek)),
        graphql_name="weeklyRepeatDays",
    )


class AlertsNotificationChannelCreateError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "error_type")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    error_type = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNotificationChannelCreateErrorType),
        graphql_name="errorType",
    )


class AlertsNotificationChannelCreateResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error", "notification_channel")
    error = sgqlc.types.Field(
        AlertsNotificationChannelCreateError, graphql_name="error"
    )

    notification_channel = sgqlc.types.Field(
        "AlertsNotificationChannelMutation", graphql_name="notificationChannel"
    )


class AlertsNotificationChannelDeleteError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "error_type", "notification_channel_id")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    error_type = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNotificationChannelDeleteErrorType),
        graphql_name="errorType",
    )

    notification_channel_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="notificationChannelId"
    )


class AlertsNotificationChannelDeleteResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error", "id")
    error = sgqlc.types.Field(
        AlertsNotificationChannelDeleteError, graphql_name="error"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class AlertsNotificationChannelId(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ()


class AlertsNotificationChannelPoliciesResultSet(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("policies", "total_count")
    policies = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("AlertsNotificationChannelPolicy"))
        ),
        graphql_name="policies",
    )

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AlertsNotificationChannelPolicy(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "name")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class AlertsNotificationChannelUpdateError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "error_type", "notification_channel_id")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    error_type = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNotificationChannelUpdateErrorType),
        graphql_name="errorType",
    )

    notification_channel_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="notificationChannelId"
    )


class AlertsNotificationChannelUpdateResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error", "notification_channel")
    error = sgqlc.types.Field(
        AlertsNotificationChannelUpdateError, graphql_name="error"
    )

    notification_channel = sgqlc.types.Field(
        "AlertsNotificationChannelMutation", graphql_name="notificationChannel"
    )


class AlertsNotificationChannelsAddToPolicyError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "error_type", "notification_channel_id")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    error_type = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNotificationChannelsAddToPolicyErrorType),
        graphql_name="errorType",
    )

    notification_channel_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="notificationChannelId"
    )


class AlertsNotificationChannelsAddToPolicyResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "notification_channels", "policy_id")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(AlertsNotificationChannelsAddToPolicyError)
            )
        ),
        graphql_name="errors",
    )

    notification_channels = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AlertsNotificationChannelId))
        ),
        graphql_name="notificationChannels",
    )

    policy_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="policyId")


class AlertsNotificationChannelsRemoveFromPolicyError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "error_type", "notification_channel_id")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    error_type = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNotificationChannelsRemoveFromPolicyErrorType),
        graphql_name="errorType",
    )

    notification_channel_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="notificationChannelId"
    )


class AlertsNotificationChannelsRemoveFromPolicyResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "notification_channels", "policy_id")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(AlertsNotificationChannelsRemoveFromPolicyError)
            )
        ),
        graphql_name="errors",
    )

    notification_channels = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AlertsNotificationChannelId))
        ),
        graphql_name="notificationChannels",
    )

    policy_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="policyId")


class AlertsNotificationChannelsResultSet(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("channels", "next_cursor", "total_count")
    channels = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AlertsNotificationChannel))
        ),
        graphql_name="channels",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AlertsNrqlConditionExpiration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "close_violations_on_expiration",
        "expiration_duration",
        "open_violation_on_expiration",
    )
    close_violations_on_expiration = sgqlc.types.Field(
        Boolean, graphql_name="closeViolationsOnExpiration"
    )

    expiration_duration = sgqlc.types.Field(Seconds, graphql_name="expirationDuration")

    open_violation_on_expiration = sgqlc.types.Field(
        Boolean, graphql_name="openViolationOnExpiration"
    )


class AlertsNrqlConditionQuery(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("query",)
    query = sgqlc.types.Field(sgqlc.types.non_null(Nrql), graphql_name="query")


class AlertsNrqlConditionSignal(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "aggregation_delay",
        "aggregation_method",
        "aggregation_timer",
        "aggregation_window",
        "evaluation_delay",
        "fill_option",
        "fill_value",
        "slide_by",
    )
    aggregation_delay = sgqlc.types.Field(Seconds, graphql_name="aggregationDelay")

    aggregation_method = sgqlc.types.Field(
        AlertsSignalAggregationMethod, graphql_name="aggregationMethod"
    )

    aggregation_timer = sgqlc.types.Field(Seconds, graphql_name="aggregationTimer")

    aggregation_window = sgqlc.types.Field(Seconds, graphql_name="aggregationWindow")

    evaluation_delay = sgqlc.types.Field(Seconds, graphql_name="evaluationDelay")

    fill_option = sgqlc.types.Field(AlertsFillOption, graphql_name="fillOption")

    fill_value = sgqlc.types.Field(Float, graphql_name="fillValue")

    slide_by = sgqlc.types.Field(Seconds, graphql_name="slideBy")


class AlertsNrqlConditionTerms(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "operator",
        "priority",
        "threshold",
        "threshold_duration",
        "threshold_occurrences",
    )
    operator = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNrqlConditionTermsOperator), graphql_name="operator"
    )

    priority = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNrqlConditionPriority), graphql_name="priority"
    )

    threshold = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name="threshold")

    threshold_duration = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="thresholdDuration"
    )

    threshold_occurrences = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNrqlConditionThresholdOccurrences),
        graphql_name="thresholdOccurrences",
    )


class AlertsNrqlConditionsSearchResultSet(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "nrql_conditions", "total_count")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    nrql_conditions = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AlertsNrqlCondition))
        ),
        graphql_name="nrqlConditions",
    )

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AlertsOpsGenieNotificationChannelConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("api_key", "data_center_region", "recipients", "tags", "teams")
    api_key = sgqlc.types.Field(
        sgqlc.types.non_null(SecureValue), graphql_name="apiKey"
    )

    data_center_region = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsOpsGenieDataCenterRegion),
        graphql_name="dataCenterRegion",
    )

    recipients = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="recipients"
    )

    tags = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="tags"
    )

    teams = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="teams"
    )


class AlertsPagerDutyNotificationChannelConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("api_key",)
    api_key = sgqlc.types.Field(
        sgqlc.types.non_null(SecureValue), graphql_name="apiKey"
    )


class AlertsPoliciesSearchResultSet(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "policies", "total_count")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    policies = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("AlertsPolicy"))),
        graphql_name="policies",
    )

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AlertsPolicy(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "id", "incident_preference", "name")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    incident_preference = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsIncidentPreference),
        graphql_name="incidentPreference",
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class AlertsPolicyDeleteResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class AlertsSlackNotificationChannelConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("team_channel", "url")
    team_channel = sgqlc.types.Field(String, graphql_name="teamChannel")

    url = sgqlc.types.Field(sgqlc.types.non_null(SecureValue), graphql_name="url")


class AlertsUserNotificationChannelConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ()


class AlertsVictorOpsNotificationChannelConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("key", "route_key")
    key = sgqlc.types.Field(sgqlc.types.non_null(SecureValue), graphql_name="key")

    route_key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="routeKey")


class AlertsWebhookBasicAuthInput(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("password", "username")
    password = sgqlc.types.Field(
        sgqlc.types.non_null(SecureValue), graphql_name="password"
    )

    username = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="username")


class AlertsWebhookCustomHeaderInput(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(SecureValue), graphql_name="value")


class AlertsWebhookNotificationChannelConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "base_url",
        "basic_auth",
        "custom_http_headers",
        "custom_payload_body",
        "custom_payload_type",
    )
    base_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="baseUrl")

    basic_auth = sgqlc.types.Field(
        AlertsWebhookBasicAuthInput, graphql_name="basicAuth"
    )

    custom_http_headers = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(AlertsWebhookCustomHeaderInput)),
        graphql_name="customHttpHeaders",
    )

    custom_payload_body = sgqlc.types.Field(String, graphql_name="customPayloadBody")

    custom_payload_type = sgqlc.types.Field(
        AlertsWebhookCustomPayloadType, graphql_name="customPayloadType"
    )


class AlertsXMattersNotificationChannelConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("integration_url",)
    integration_url = sgqlc.types.Field(
        sgqlc.types.non_null(SecureValue), graphql_name="integrationUrl"
    )


class ApiAccessActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("key", "key_search")
    key = sgqlc.types.Field(
        ApiAccessKey,
        graphql_name="key",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
                (
                    "key_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ApiAccessKeyType),
                        graphql_name="keyType",
                        default=None,
                    ),
                ),
            )
        ),
    )

    key_search = sgqlc.types.Field(
        "ApiAccessKeySearchResult",
        graphql_name="keySearch",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "query",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ApiAccessKeySearchQuery),
                        graphql_name="query",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `query` (`ApiAccessKeySearchQuery!`)
    """


class ApiAccessCreateKeyResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("created_keys", "errors")
    created_keys = sgqlc.types.Field(
        sgqlc.types.list_of(ApiAccessKey), graphql_name="createdKeys"
    )

    errors = sgqlc.types.Field(
        sgqlc.types.list_of(ApiAccessKeyError), graphql_name="errors"
    )


class ApiAccessDeleteKeyResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("deleted_keys", "errors")
    deleted_keys = sgqlc.types.Field(
        sgqlc.types.list_of("ApiAccessDeletedKey"), graphql_name="deletedKeys"
    )

    errors = sgqlc.types.Field(
        sgqlc.types.list_of(ApiAccessKeyError), graphql_name="errors"
    )


class ApiAccessDeletedKey(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id",)
    id = sgqlc.types.Field(String, graphql_name="id")


class ApiAccessKeySearchResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "keys", "next_cursor")
    count = sgqlc.types.Field(Int, graphql_name="count")

    keys = sgqlc.types.Field(sgqlc.types.list_of(ApiAccessKey), graphql_name="keys")

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")


class ApiAccessUpdateKeyResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "updated_keys")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(ApiAccessKeyError), graphql_name="errors"
    )

    updated_keys = sgqlc.types.Field(
        sgqlc.types.list_of(ApiAccessKey), graphql_name="updatedKeys"
    )


class ApmApplicationDeployment(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "changelog",
        "description",
        "permalink",
        "revision",
        "timestamp",
        "user",
    )
    changelog = sgqlc.types.Field(String, graphql_name="changelog")

    description = sgqlc.types.Field(String, graphql_name="description")

    permalink = sgqlc.types.Field(String, graphql_name="permalink")

    revision = sgqlc.types.Field(String, graphql_name="revision")

    timestamp = sgqlc.types.Field(EpochMilliseconds, graphql_name="timestamp")

    user = sgqlc.types.Field(String, graphql_name="user")


class ApmApplicationEntitySettingsResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entity",)
    entity = sgqlc.types.Field("ApmApplicationEntity", graphql_name="entity")


class ApmApplicationRunningAgentVersions(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("max_version", "min_version")
    max_version = sgqlc.types.Field(String, graphql_name="maxVersion")

    min_version = sgqlc.types.Field(String, graphql_name="minVersion")


class ApmApplicationSettings(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("apdex_target", "server_side_config")
    apdex_target = sgqlc.types.Field(Float, graphql_name="apdexTarget")

    server_side_config = sgqlc.types.Field(Boolean, graphql_name="serverSideConfig")


class ApmApplicationSummaryData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "apdex_score",
        "error_rate",
        "host_count",
        "instance_count",
        "non_web_response_time_average",
        "non_web_throughput",
        "response_time_average",
        "throughput",
        "web_response_time_average",
        "web_throughput",
    )
    apdex_score = sgqlc.types.Field(Float, graphql_name="apdexScore")

    error_rate = sgqlc.types.Field(Float, graphql_name="errorRate")

    host_count = sgqlc.types.Field(Int, graphql_name="hostCount")

    instance_count = sgqlc.types.Field(Int, graphql_name="instanceCount")

    non_web_response_time_average = sgqlc.types.Field(
        Seconds, graphql_name="nonWebResponseTimeAverage"
    )

    non_web_throughput = sgqlc.types.Field(Float, graphql_name="nonWebThroughput")

    response_time_average = sgqlc.types.Field(
        Seconds, graphql_name="responseTimeAverage"
    )

    throughput = sgqlc.types.Field(Float, graphql_name="throughput")

    web_response_time_average = sgqlc.types.Field(
        Seconds, graphql_name="webResponseTimeAverage"
    )

    web_throughput = sgqlc.types.Field(Float, graphql_name="webThroughput")


class ApmBrowserApplicationSummaryData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "ajax_request_throughput",
        "ajax_response_time_average",
        "js_error_rate",
        "page_load_throughput",
        "page_load_time_average",
    )
    ajax_request_throughput = sgqlc.types.Field(
        Float, graphql_name="ajaxRequestThroughput"
    )

    ajax_response_time_average = sgqlc.types.Field(
        Seconds, graphql_name="ajaxResponseTimeAverage"
    )

    js_error_rate = sgqlc.types.Field(Float, graphql_name="jsErrorRate")

    page_load_throughput = sgqlc.types.Field(Float, graphql_name="pageLoadThroughput")

    page_load_time_average = sgqlc.types.Field(
        Float, graphql_name="pageLoadTimeAverage"
    )


class ApmExternalServiceSummaryData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("response_time_average", "throughput")
    response_time_average = sgqlc.types.Field(
        Seconds, graphql_name="responseTimeAverage"
    )

    throughput = sgqlc.types.Field(Float, graphql_name="throughput")


class AuthorizationManagementAuthenticationDomain(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("groups", "id", "name")
    groups = sgqlc.types.Field(
        sgqlc.types.non_null("AuthorizationManagementGroupSearch"),
        graphql_name="groups",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `id` (`[ID!]`)
    """

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class AuthorizationManagementAuthenticationDomainSearch(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("authentication_domains", "next_cursor", "total_count")
    authentication_domains = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(AuthorizationManagementAuthenticationDomain)
            )
        ),
        graphql_name="authenticationDomains",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AuthorizationManagementGrantAccessPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("roles",)
    roles = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null("AuthorizationManagementGrantedRole")
            )
        ),
        graphql_name="roles",
    )


class AuthorizationManagementGrantedRole(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "display_name",
        "group_id",
        "id",
        "name",
        "organization_id",
        "role_id",
        "type",
    )
    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    group_id = sgqlc.types.Field(ID, graphql_name="groupId")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    organization_id = sgqlc.types.Field(ID, graphql_name="organizationId")

    role_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="roleId")

    type = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="type")


class AuthorizationManagementGrantedRoleSearch(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "roles", "total_count")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    roles = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(AuthorizationManagementGrantedRole)
            )
        ),
        graphql_name="roles",
    )

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AuthorizationManagementGroup(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("display_name", "id", "roles")
    display_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="displayName"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    roles = sgqlc.types.Field(
        sgqlc.types.non_null(AuthorizationManagementGrantedRoleSearch),
        graphql_name="roles",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="id",
                        default=None,
                    ),
                ),
                (
                    "role_id",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="roleId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `id` (`[ID!]`)
    * `role_id` (`[ID!]`)
    """


class AuthorizationManagementGroupSearch(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("groups", "next_cursor", "total_count")
    groups = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AuthorizationManagementGroup))
        ),
        graphql_name="groups",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class AuthorizationManagementOrganizationStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("authentication_domains", "roles")
    authentication_domains = sgqlc.types.Field(
        AuthorizationManagementAuthenticationDomainSearch,
        graphql_name="authenticationDomains",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `id` (`[ID!]`)
    """

    roles = sgqlc.types.Field(
        "AuthorizationManagementRoleSearch",
        graphql_name="roles",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `id` (`[ID!]`)
    """


class AuthorizationManagementRevokeAccessPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("roles",)
    roles = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(AuthorizationManagementGrantedRole)
            )
        ),
        graphql_name="roles",
    )


class AuthorizationManagementRole(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("display_name", "id", "name", "scope", "type")
    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    scope = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="scope")

    type = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="type")


class AuthorizationManagementRoleSearch(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "roles", "total_count")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    roles = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(AuthorizationManagementRole))
        ),
        graphql_name="roles",
    )

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class BrowserApplicationRunningAgentVersions(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "max_semantic_version",
        "max_version",
        "min_semantic_version",
        "min_version",
    )
    max_semantic_version = sgqlc.types.Field(SemVer, graphql_name="maxSemanticVersion")

    max_version = sgqlc.types.Field(Int, graphql_name="maxVersion")

    min_semantic_version = sgqlc.types.Field(SemVer, graphql_name="minSemanticVersion")

    min_version = sgqlc.types.Field(Int, graphql_name="minVersion")


class BrowserApplicationSettings(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("apdex_target",)
    apdex_target = sgqlc.types.Field(Float, graphql_name="apdexTarget")


class BrowserApplicationSummaryData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "ajax_request_throughput",
        "ajax_response_time_average",
        "js_error_rate",
        "page_load_throughput",
        "page_load_time_average",
        "page_load_time_median",
        "spa_response_time_average",
        "spa_response_time_median",
    )
    ajax_request_throughput = sgqlc.types.Field(
        Float, graphql_name="ajaxRequestThroughput"
    )

    ajax_response_time_average = sgqlc.types.Field(
        Seconds, graphql_name="ajaxResponseTimeAverage"
    )

    js_error_rate = sgqlc.types.Field(Float, graphql_name="jsErrorRate")

    page_load_throughput = sgqlc.types.Field(Float, graphql_name="pageLoadThroughput")

    page_load_time_average = sgqlc.types.Field(
        Float, graphql_name="pageLoadTimeAverage"
    )

    page_load_time_median = sgqlc.types.Field(Float, graphql_name="pageLoadTimeMedian")

    spa_response_time_average = sgqlc.types.Field(
        Seconds, graphql_name="spaResponseTimeAverage"
    )

    spa_response_time_median = sgqlc.types.Field(
        Seconds, graphql_name="spaResponseTimeMedian"
    )


class ChangeTrackingDeployment(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "changelog",
        "commit",
        "deep_link",
        "deployment_id",
        "deployment_type",
        "description",
        "entity_guid",
        "group_id",
        "timestamp",
        "user",
        "version",
    )
    changelog = sgqlc.types.Field(String, graphql_name="changelog")

    commit = sgqlc.types.Field(String, graphql_name="commit")

    deep_link = sgqlc.types.Field(String, graphql_name="deepLink")

    deployment_id = sgqlc.types.Field(String, graphql_name="deploymentId")

    deployment_type = sgqlc.types.Field(
        ChangeTrackingDeploymentType, graphql_name="deploymentType"
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    entity_guid = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGuid), graphql_name="entityGuid"
    )

    group_id = sgqlc.types.Field(String, graphql_name="groupId")

    timestamp = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="timestamp"
    )

    user = sgqlc.types.Field(String, graphql_name="user")

    version = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="version")


class ChangeTrackingDeploymentSearchResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("results",)
    results = sgqlc.types.Field(
        sgqlc.types.list_of(ChangeTrackingDeployment), graphql_name="results"
    )


class CloudAccountFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("linked_account", "linked_accounts", "provider", "providers")
    linked_account = sgqlc.types.Field(
        "CloudLinkedAccount",
        graphql_name="linkedAccount",
        args=sgqlc.types.ArgDict(
            (("id", sgqlc.types.Arg(Int, graphql_name="id", default=None)),)
        ),
    )

    linked_accounts = sgqlc.types.Field(
        sgqlc.types.list_of("CloudLinkedAccount"), graphql_name="linkedAccounts"
    )

    provider = sgqlc.types.Field(
        CloudProvider,
        graphql_name="provider",
        args=sgqlc.types.ArgDict(
            (("slug", sgqlc.types.Arg(String, graphql_name="slug", default=None)),)
        ),
    )

    providers = sgqlc.types.Field(
        sgqlc.types.list_of(CloudProvider), graphql_name="providers"
    )


class CloudAccountMutationError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "linked_account_id",
        "message",
        "nr_account_id",
        "provider_slug",
        "type",
    )
    linked_account_id = sgqlc.types.Field(Int, graphql_name="linkedAccountId")

    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    nr_account_id = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="nrAccountId"
    )

    provider_slug = sgqlc.types.Field(String, graphql_name="providerSlug")

    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")


class CloudActorFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("linked_accounts",)
    linked_accounts = sgqlc.types.Field(
        sgqlc.types.list_of("CloudLinkedAccount"),
        graphql_name="linkedAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "provider",
                    sgqlc.types.Arg(String, graphql_name="provider", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `provider` (`String`)
    """


class CloudConfigureIntegrationPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "integrations")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("CloudIntegrationMutationError"))
        ),
        graphql_name="errors",
    )

    integrations = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(CloudIntegration))
        ),
        graphql_name="integrations",
    )


class CloudDisableIntegrationPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("disabled_integrations", "errors")
    disabled_integrations = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(CloudIntegration))
        ),
        graphql_name="disabledIntegrations",
    )

    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("CloudIntegrationMutationError"))
        ),
        graphql_name="errors",
    )


class CloudIntegrationMutationError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "integration_slug",
        "linked_account_id",
        "message",
        "nr_account_id",
        "type",
    )
    integration_slug = sgqlc.types.Field(String, graphql_name="integrationSlug")

    linked_account_id = sgqlc.types.Field(Int, graphql_name="linkedAccountId")

    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    nr_account_id = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="nrAccountId"
    )

    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")


class CloudLinkAccountPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "linked_accounts")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(CloudAccountMutationError))
        ),
        graphql_name="errors",
    )

    linked_accounts = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("CloudLinkedAccount"))
        ),
        graphql_name="linkedAccounts",
    )


class CloudLinkedAccount(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "auth_label",
        "created_at",
        "disabled",
        "external_id",
        "id",
        "integration",
        "integrations",
        "metric_collection_mode",
        "name",
        "nr_account_id",
        "provider",
        "updated_at",
    )
    auth_label = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="authLabel"
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochSeconds), graphql_name="createdAt"
    )

    disabled = sgqlc.types.Field(Boolean, graphql_name="disabled")

    external_id = sgqlc.types.Field(String, graphql_name="externalId")

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    integration = sgqlc.types.Field(
        sgqlc.types.non_null(CloudIntegration),
        graphql_name="integration",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    integrations = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(CloudIntegration))
        ),
        graphql_name="integrations",
        args=sgqlc.types.ArgDict(
            (
                (
                    "service",
                    sgqlc.types.Arg(String, graphql_name="service", default=None),
                ),
            )
        ),
    )

    metric_collection_mode = sgqlc.types.Field(
        sgqlc.types.non_null(CloudMetricCollectionMode),
        graphql_name="metricCollectionMode",
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    nr_account_id = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="nrAccountId"
    )

    provider = sgqlc.types.Field(
        sgqlc.types.non_null(CloudProvider), graphql_name="provider"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochSeconds), graphql_name="updatedAt"
    )


class CloudMigrateAwsGovCloudToAssumeRolePayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "linked_accounts")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(CloudAccountMutationError))
        ),
        graphql_name="errors",
    )

    linked_accounts = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(CloudLinkedAccount))
        ),
        graphql_name="linkedAccounts",
    )


class CloudRenameAccountPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "linked_accounts")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(CloudAccountMutationError))
        ),
        graphql_name="errors",
    )

    linked_accounts = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(CloudLinkedAccount))
        ),
        graphql_name="linkedAccounts",
    )


class CloudService(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "icon",
        "id",
        "is_enabled",
        "name",
        "provider",
        "slug",
        "updated_at",
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochSeconds), graphql_name="createdAt"
    )

    icon = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="icon")

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    is_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="isEnabled"
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    provider = sgqlc.types.Field(
        sgqlc.types.non_null(CloudProvider), graphql_name="provider"
    )

    slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="slug")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochSeconds), graphql_name="updatedAt"
    )


class CloudUnlinkAccountPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "unlinked_accounts")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(CloudAccountMutationError))
        ),
        graphql_name="errors",
    )

    unlinked_accounts = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(CloudLinkedAccount))
        ),
        graphql_name="unlinkedAccounts",
    )


class CrossAccountNrdbResultContainer(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "current_results",
        "metadata",
        "nrql",
        "other_result",
        "previous_results",
        "query_progress",
        "raw_response",
        "results",
        "total_result",
    )
    current_results = sgqlc.types.Field(
        sgqlc.types.list_of(NrdbResult), graphql_name="currentResults"
    )

    metadata = sgqlc.types.Field("NrdbMetadata", graphql_name="metadata")

    nrql = sgqlc.types.Field(Nrql, graphql_name="nrql")

    other_result = sgqlc.types.Field(NrdbResult, graphql_name="otherResult")

    previous_results = sgqlc.types.Field(
        sgqlc.types.list_of(NrdbResult), graphql_name="previousResults"
    )

    query_progress = sgqlc.types.Field(
        "NrdbQueryProgress", graphql_name="queryProgress"
    )

    raw_response = sgqlc.types.Field(NrdbRawResults, graphql_name="rawResponse")

    results = sgqlc.types.Field(sgqlc.types.list_of(NrdbResult), graphql_name="results")

    total_result = sgqlc.types.Field(NrdbResult, graphql_name="totalResult")


class DashboardActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("live_urls",)
    live_urls = sgqlc.types.Field(
        "DashboardLiveUrlResult",
        graphql_name="liveUrls",
        args=sgqlc.types.ArgDict(
            (
                (
                    "filter",
                    sgqlc.types.Arg(
                        DashboardLiveUrlsFilterInput,
                        graphql_name="filter",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `filter` (`DashboardLiveUrlsFilterInput`)
    """


class DashboardAddWidgetsToPageError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(DashboardAddWidgetsToPageErrorType), graphql_name="type"
    )


class DashboardAddWidgetsToPageResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardAddWidgetsToPageError), graphql_name="errors"
    )


class DashboardAreaWidgetConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nrql_queries",)
    nrql_queries = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardWidgetNrqlQuery"), graphql_name="nrqlQueries"
    )


class DashboardBarWidgetConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nrql_queries",)
    nrql_queries = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardWidgetNrqlQuery"), graphql_name="nrqlQueries"
    )


class DashboardBillboardWidgetConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nrql_queries", "thresholds")
    nrql_queries = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardWidgetNrqlQuery"), graphql_name="nrqlQueries"
    )

    thresholds = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardBillboardWidgetThreshold"),
        graphql_name="thresholds",
    )


class DashboardBillboardWidgetThreshold(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("alert_severity", "value")
    alert_severity = sgqlc.types.Field(
        DashboardAlertSeverity, graphql_name="alertSeverity"
    )

    value = sgqlc.types.Field(Float, graphql_name="value")


class DashboardCreateError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(DashboardCreateErrorType), graphql_name="type"
    )


class DashboardCreateResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entity_result", "errors")
    entity_result = sgqlc.types.Field(
        "DashboardEntityResult", graphql_name="entityResult"
    )

    errors = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardCreateError), graphql_name="errors"
    )


class DashboardDeleteError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(DashboardDeleteErrorType), graphql_name="type"
    )


class DashboardDeleteResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "status")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardDeleteError), graphql_name="errors"
    )

    status = sgqlc.types.Field(DashboardDeleteResultStatus, graphql_name="status")


class DashboardEntityOwnerInfo(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("email", "user_id")
    email = sgqlc.types.Field(String, graphql_name="email")

    user_id = sgqlc.types.Field(Int, graphql_name="userId")


class DashboardEntityResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "created_at",
        "description",
        "guid",
        "name",
        "owner",
        "pages",
        "permissions",
        "updated_at",
        "variables",
    )
    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")

    description = sgqlc.types.Field(String, graphql_name="description")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    name = sgqlc.types.Field(String, graphql_name="name")

    owner = sgqlc.types.Field("DashboardOwnerInfo", graphql_name="owner")

    pages = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardPage"), graphql_name="pages"
    )

    permissions = sgqlc.types.Field(DashboardPermissions, graphql_name="permissions")

    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")

    variables = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardVariable"), graphql_name="variables"
    )


class DashboardLineWidgetConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nrql_queries",)
    nrql_queries = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardWidgetNrqlQuery"), graphql_name="nrqlQueries"
    )


class DashboardLiveUrl(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("created_at", "title", "type", "url", "uuid")
    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    title = sgqlc.types.Field(String, graphql_name="title")

    type = sgqlc.types.Field(DashboardLiveUrlType, graphql_name="type")

    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")

    uuid = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="uuid")


class DashboardLiveUrlError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(DashboardLiveUrlErrorType, graphql_name="type")


class DashboardLiveUrlResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "live_urls")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardLiveUrlError), graphql_name="errors"
    )

    live_urls = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardLiveUrl), graphql_name="liveUrls"
    )


class DashboardMarkdownWidgetConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("text",)
    text = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="text")


class DashboardOwnerInfo(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("email", "user_id")
    email = sgqlc.types.Field(String, graphql_name="email")

    user_id = sgqlc.types.Field(Int, graphql_name="userId")


class DashboardPage(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "description",
        "guid",
        "name",
        "owner",
        "updated_at",
        "widgets",
    )
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")

    description = sgqlc.types.Field(String, graphql_name="description")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    name = sgqlc.types.Field(String, graphql_name="name")

    owner = sgqlc.types.Field(DashboardOwnerInfo, graphql_name="owner")

    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")

    widgets = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardWidget"), graphql_name="widgets"
    )


class DashboardPieWidgetConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nrql_queries",)
    nrql_queries = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardWidgetNrqlQuery"), graphql_name="nrqlQueries"
    )


class DashboardRevokeLiveUrlResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "uuid")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardLiveUrlError), graphql_name="errors"
    )

    uuid = sgqlc.types.Field(ID, graphql_name="uuid")


class DashboardTableWidgetConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nrql_queries",)
    nrql_queries = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardWidgetNrqlQuery"), graphql_name="nrqlQueries"
    )


class DashboardUndeleteError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(DashboardUndeleteErrorType), graphql_name="type"
    )


class DashboardUndeleteResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardUndeleteError), graphql_name="errors"
    )


class DashboardUpdateError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(DashboardUpdateErrorType), graphql_name="type"
    )


class DashboardUpdatePageError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(DashboardUpdatePageErrorType), graphql_name="type"
    )


class DashboardUpdatePageResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardUpdatePageError), graphql_name="errors"
    )


class DashboardUpdateResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entity_result", "errors")
    entity_result = sgqlc.types.Field(
        DashboardEntityResult, graphql_name="entityResult"
    )

    errors = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardUpdateError), graphql_name="errors"
    )


class DashboardUpdateWidgetsInPageError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(String, graphql_name="description")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(DashboardUpdateWidgetsInPageErrorType), graphql_name="type"
    )


class DashboardUpdateWidgetsInPageResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardUpdateWidgetsInPageError), graphql_name="errors"
    )


class DashboardVariable(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "default_values",
        "is_multi_selection",
        "items",
        "name",
        "nrql_query",
        "replacement_strategy",
        "title",
        "type",
    )
    default_values = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardVariableDefaultItem"),
        graphql_name="defaultValues",
    )

    is_multi_selection = sgqlc.types.Field(Boolean, graphql_name="isMultiSelection")

    items = sgqlc.types.Field(
        sgqlc.types.list_of("DashboardVariableEnumItem"), graphql_name="items"
    )

    name = sgqlc.types.Field(String, graphql_name="name")

    nrql_query = sgqlc.types.Field(
        "DashboardVariableNrqlQuery", graphql_name="nrqlQuery"
    )

    replacement_strategy = sgqlc.types.Field(
        DashboardVariableReplacementStrategy, graphql_name="replacementStrategy"
    )

    title = sgqlc.types.Field(String, graphql_name="title")

    type = sgqlc.types.Field(DashboardVariableType, graphql_name="type")


class DashboardVariableDefaultItem(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("value",)
    value = sgqlc.types.Field("DashboardVariableDefaultValue", graphql_name="value")


class DashboardVariableDefaultValue(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("string",)
    string = sgqlc.types.Field(String, graphql_name="string")


class DashboardVariableEnumItem(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("title", "value")
    title = sgqlc.types.Field(String, graphql_name="title")

    value = sgqlc.types.Field(String, graphql_name="value")


class DashboardVariableNrqlQuery(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_ids", "query")
    account_ids = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name="accountIds")

    query = sgqlc.types.Field(sgqlc.types.non_null(Nrql), graphql_name="query")


class DashboardWidget(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "configuration",
        "id",
        "layout",
        "linked_entities",
        "raw_configuration",
        "title",
        "visualization",
    )
    configuration = sgqlc.types.Field(
        "DashboardWidgetConfiguration", graphql_name="configuration"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    layout = sgqlc.types.Field("DashboardWidgetLayout", graphql_name="layout")

    linked_entities = sgqlc.types.Field(
        sgqlc.types.list_of(EntityOutline), graphql_name="linkedEntities"
    )

    raw_configuration = sgqlc.types.Field(
        sgqlc.types.non_null(DashboardWidgetRawConfiguration),
        graphql_name="rawConfiguration",
    )

    title = sgqlc.types.Field(String, graphql_name="title")

    visualization = sgqlc.types.Field(
        sgqlc.types.non_null("DashboardWidgetVisualization"),
        graphql_name="visualization",
    )


class DashboardWidgetConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("area", "bar", "billboard", "line", "markdown", "pie", "table")
    area = sgqlc.types.Field(DashboardAreaWidgetConfiguration, graphql_name="area")

    bar = sgqlc.types.Field(DashboardBarWidgetConfiguration, graphql_name="bar")

    billboard = sgqlc.types.Field(
        DashboardBillboardWidgetConfiguration, graphql_name="billboard"
    )

    line = sgqlc.types.Field(DashboardLineWidgetConfiguration, graphql_name="line")

    markdown = sgqlc.types.Field(
        DashboardMarkdownWidgetConfiguration, graphql_name="markdown"
    )

    pie = sgqlc.types.Field(DashboardPieWidgetConfiguration, graphql_name="pie")

    table = sgqlc.types.Field(DashboardTableWidgetConfiguration, graphql_name="table")


class DashboardWidgetLayout(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("column", "height", "row", "width")
    column = sgqlc.types.Field(Int, graphql_name="column")

    height = sgqlc.types.Field(Int, graphql_name="height")

    row = sgqlc.types.Field(Int, graphql_name="row")

    width = sgqlc.types.Field(Int, graphql_name="width")


class DashboardWidgetNrqlQuery(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "query")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    query = sgqlc.types.Field(sgqlc.types.non_null(Nrql), graphql_name="query")


class DashboardWidgetVisualization(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id",)
    id = sgqlc.types.Field(String, graphql_name="id")


class DataDictionaryAttribute(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("definition", "docs_url", "name", "units")
    definition = sgqlc.types.Field(
        sgqlc.types.non_null(String),
        graphql_name="definition",
        args=sgqlc.types.ArgDict(
            (
                (
                    "format",
                    sgqlc.types.Arg(
                        DataDictionaryTextFormat, graphql_name="format", default="PLAIN"
                    ),
                ),
            )
        ),
    )

    docs_url = sgqlc.types.Field(String, graphql_name="docsUrl")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    units = sgqlc.types.Field("DataDictionaryUnit", graphql_name="units")


class DataDictionaryDataSource(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("name",)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class DataDictionaryDocsStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("events",)
    events = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("DataDictionaryEvent"))
        ),
        graphql_name="events",
        args=sgqlc.types.ArgDict(
            (
                (
                    "names",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(String), graphql_name="names", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `names` (`[String]`)
    """


class DataDictionaryEvent(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attributes", "data_sources", "definition", "name")
    attributes = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(DataDictionaryAttribute))
        ),
        graphql_name="attributes",
    )

    data_sources = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(DataDictionaryDataSource))
        ),
        graphql_name="dataSources",
    )

    definition = sgqlc.types.Field(
        String,
        graphql_name="definition",
        args=sgqlc.types.ArgDict(
            (
                (
                    "format",
                    sgqlc.types.Arg(
                        DataDictionaryTextFormat, graphql_name="format", default="PLAIN"
                    ),
                ),
            )
        ),
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class DataDictionaryUnit(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("label",)
    label = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="label")


class DataManagementAccountLimit(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "category",
        "description",
        "documentation_link",
        "limit_reached_behavior_description",
        "name",
        "time_interval",
        "unit",
        "value",
    )
    category = sgqlc.types.Field(DataManagementCategory, graphql_name="category")

    description = sgqlc.types.Field(String, graphql_name="description")

    documentation_link = sgqlc.types.Field(String, graphql_name="documentationLink")

    limit_reached_behavior_description = sgqlc.types.Field(
        String, graphql_name="limitReachedBehaviorDescription"
    )

    name = sgqlc.types.Field(String, graphql_name="name")

    time_interval = sgqlc.types.Field(Nrql, graphql_name="timeInterval")

    unit = sgqlc.types.Field(DataManagementUnit, graphql_name="unit")

    value = sgqlc.types.Field(Int, graphql_name="value")


class DataManagementAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "customizable_retention",
        "event_retention_policies",
        "event_retention_rule",
        "event_retention_rules",
        "feature_settings",
        "limits",
        "retention_audit",
        "retentions",
    )
    customizable_retention = sgqlc.types.Field(
        "DataManagementCustomizableRetention", graphql_name="customizableRetention"
    )

    event_retention_policies = sgqlc.types.Field(
        sgqlc.types.list_of("DataManagementRenderedRetention"),
        graphql_name="eventRetentionPolicies",
    )

    event_retention_rule = sgqlc.types.Field(
        "DataManagementRule",
        graphql_name="eventRetentionRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "namespace",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="namespace",
                        default=None,
                    ),
                ),
            )
        ),
    )

    event_retention_rules = sgqlc.types.Field(
        sgqlc.types.list_of("DataManagementRule"), graphql_name="eventRetentionRules"
    )

    feature_settings = sgqlc.types.Field(
        sgqlc.types.list_of("DataManagementFeatureSetting"),
        graphql_name="featureSettings",
    )

    limits = sgqlc.types.Field(
        sgqlc.types.list_of(DataManagementAccountLimit), graphql_name="limits"
    )

    retention_audit = sgqlc.types.Field(
        sgqlc.types.list_of("DataManagementRetentionValues"),
        graphql_name="retentionAudit",
    )

    retentions = sgqlc.types.Field(
        sgqlc.types.list_of("DataManagementRetention"), graphql_name="retentions"
    )


class DataManagementAppliedRules(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "retention_in_days")
    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    retention_in_days = sgqlc.types.Field(Int, graphql_name="retentionInDays")


class DataManagementBulkCopyResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("failure", "success")
    failure = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name="failure")

    success = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name="success")


class DataManagementCustomizableRetention(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("event_namespaces",)
    event_namespaces = sgqlc.types.Field(
        sgqlc.types.list_of("DataManagementEventNamespaces"),
        graphql_name="eventNamespaces",
    )


class DataManagementEventNamespaces(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("max_retention_in_days", "min_retention_in_days", "namespace")
    max_retention_in_days = sgqlc.types.Field(Int, graphql_name="maxRetentionInDays")

    min_retention_in_days = sgqlc.types.Field(Int, graphql_name="minRetentionInDays")

    namespace = sgqlc.types.Field(String, graphql_name="namespace")


class DataManagementFeatureSetting(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("enabled", "key", "locked", "name")
    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")

    key = sgqlc.types.Field(String, graphql_name="key")

    locked = sgqlc.types.Field(Boolean, graphql_name="locked")

    name = sgqlc.types.Field(String, graphql_name="name")


class DataManagementNamespaceLevelRetention(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("retention_in_days",)
    retention_in_days = sgqlc.types.Field(Int, graphql_name="retentionInDays")


class DataManagementRenderedRetention(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "namespace",
        "namespace_level_retention",
        "updated_at",
    )
    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    namespace = sgqlc.types.Field(String, graphql_name="namespace")

    namespace_level_retention = sgqlc.types.Field(
        DataManagementNamespaceLevelRetention, graphql_name="namespaceLevelRetention"
    )

    updated_at = sgqlc.types.Field(EpochSeconds, graphql_name="updatedAt")


class DataManagementRetention(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "customizable",
        "display_name",
        "max_retention_in_days",
        "min_retention_in_days",
        "namespace",
        "source",
    )
    customizable = sgqlc.types.Field(Boolean, graphql_name="customizable")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    max_retention_in_days = sgqlc.types.Field(Int, graphql_name="maxRetentionInDays")

    min_retention_in_days = sgqlc.types.Field(Int, graphql_name="minRetentionInDays")

    namespace = sgqlc.types.Field(String, graphql_name="namespace")

    source = sgqlc.types.Field(String, graphql_name="source")


class DataManagementRetentionValues(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("applied_rules", "namespace", "subscription_retention_in_days")
    applied_rules = sgqlc.types.Field(
        sgqlc.types.list_of(DataManagementAppliedRules), graphql_name="appliedRules"
    )

    namespace = sgqlc.types.Field(String, graphql_name="namespace")

    subscription_retention_in_days = sgqlc.types.Field(
        Int, graphql_name="subscriptionRetentionInDays"
    )


class DataManagementRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "created_by_id",
        "deleted_at",
        "deleted_by_id",
        "id",
        "namespace",
        "retention_in_days",
    )
    created_at = sgqlc.types.Field(EpochSeconds, graphql_name="createdAt")

    created_by_id = sgqlc.types.Field(Int, graphql_name="createdById")

    deleted_at = sgqlc.types.Field(EpochSeconds, graphql_name="deletedAt")

    deleted_by_id = sgqlc.types.Field(Int, graphql_name="deletedById")

    id = sgqlc.types.Field(ID, graphql_name="id")

    namespace = sgqlc.types.Field(String, graphql_name="namespace")

    retention_in_days = sgqlc.types.Field(Int, graphql_name="retentionInDays")


class DateTimeWindow(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("end_time", "start_time")
    end_time = sgqlc.types.Field(DateTime, graphql_name="endTime")

    start_time = sgqlc.types.Field(DateTime, graphql_name="startTime")


class DistributedTracingActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("trace",)
    trace = sgqlc.types.Field(
        "DistributedTracingTrace",
        graphql_name="trace",
        args=sgqlc.types.ArgDict(
            (
                (
                    "timestamp",
                    sgqlc.types.Arg(
                        EpochMilliseconds, graphql_name="timestamp", default=None
                    ),
                ),
                (
                    "trace_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="traceId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `timestamp` (`EpochMilliseconds`)
    * `trace_id` (`String!`)
    """


class DistributedTracingEntityTracingSummary(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error_trace_count", "percent_of_all_error_traces")
    error_trace_count = sgqlc.types.Field(Int, graphql_name="errorTraceCount")

    percent_of_all_error_traces = sgqlc.types.Field(
        Float, graphql_name="percentOfAllErrorTraces"
    )


class DistributedTracingSpan(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "attributes",
        "client_type",
        "duration_ms",
        "entity_guid",
        "id",
        "name",
        "parent_id",
        "process_boundary",
        "span_anomalies",
        "timestamp",
        "trace_id",
    )
    attributes = sgqlc.types.Field(
        DistributedTracingSpanAttributes, graphql_name="attributes"
    )

    client_type = sgqlc.types.Field(
        DistributedTracingSpanClientType, graphql_name="clientType"
    )

    duration_ms = sgqlc.types.Field(Milliseconds, graphql_name="durationMs")

    entity_guid = sgqlc.types.Field(String, graphql_name="entityGuid")

    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    parent_id = sgqlc.types.Field(String, graphql_name="parentId")

    process_boundary = sgqlc.types.Field(
        sgqlc.types.non_null(DistributedTracingSpanProcessBoundary),
        graphql_name="processBoundary",
    )

    span_anomalies = sgqlc.types.Field(
        sgqlc.types.list_of("DistributedTracingSpanAnomaly"),
        graphql_name="spanAnomalies",
    )

    timestamp = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="timestamp"
    )

    trace_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="traceId")


class DistributedTracingSpanAnomaly(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("anomalous_value", "anomaly_type", "average_measure")
    anomalous_value = sgqlc.types.Field(
        sgqlc.types.non_null(Float), graphql_name="anomalousValue"
    )

    anomaly_type = sgqlc.types.Field(
        sgqlc.types.non_null(DistributedTracingSpanAnomalyType),
        graphql_name="anomalyType",
    )

    average_measure = sgqlc.types.Field(
        sgqlc.types.non_null(Float), graphql_name="averageMeasure"
    )


class DistributedTracingSpanConnection(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("child", "parent")
    child = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="child")

    parent = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="parent")


class DistributedTracingTrace(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "backend_duration_ms",
        "duration_ms",
        "entities",
        "entity_count",
        "id",
        "span_connections",
        "spans",
        "timestamp",
    )
    backend_duration_ms = sgqlc.types.Field(
        Milliseconds, graphql_name="backendDurationMs"
    )

    duration_ms = sgqlc.types.Field(Milliseconds, graphql_name="durationMs")

    entities = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EntityOutline))),
        graphql_name="entities",
    )

    entity_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="entityCount"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    span_connections = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(DistributedTracingSpanConnection)),
        graphql_name="spanConnections",
    )

    spans = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(DistributedTracingSpan))
        ),
        graphql_name="spans",
    )

    timestamp = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="timestamp"
    )


class DocumentationFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "agent_features",
        "agent_releases",
        "data_dictionary",
        "time_zones",
        "whats_new",
    )
    agent_features = sgqlc.types.Field(
        sgqlc.types.list_of(AgentFeatures),
        graphql_name="agentFeatures",
        args=sgqlc.types.ArgDict(
            (
                (
                    "agent_name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AgentFeaturesFilter),
                        graphql_name="agentName",
                        default=None,
                    ),
                ),
            )
        ),
    )

    agent_releases = sgqlc.types.Field(
        sgqlc.types.list_of(AgentRelease),
        graphql_name="agentReleases",
        args=sgqlc.types.ArgDict(
            (
                (
                    "agent_name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AgentReleasesFilter),
                        graphql_name="agentName",
                        default=None,
                    ),
                ),
            )
        ),
    )

    data_dictionary = sgqlc.types.Field(
        DataDictionaryDocsStitchedFields, graphql_name="dataDictionary"
    )

    time_zones = sgqlc.types.Field(
        sgqlc.types.list_of("TimeZoneInfo"), graphql_name="timeZones"
    )

    whats_new = sgqlc.types.Field("WhatsNewDocsStitchedFields", graphql_name="whatsNew")


class DomainType(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("domain", "type")
    domain = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="domain")

    type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="type")


class EdgeAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("tracing",)
    tracing = sgqlc.types.Field("EdgeTracing", graphql_name="tracing")


class EdgeCreateSpanAttributeRuleResponseError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeCreateSpanAttributeRuleResponseErrorType),
        graphql_name="type",
    )


class EdgeCreateSpanAttributeRulesResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "rules")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(EdgeCreateSpanAttributeRuleResponseError),
        graphql_name="errors",
    )

    rules = sgqlc.types.Field(
        sgqlc.types.list_of("EdgeSpanAttributeRule"), graphql_name="rules"
    )


class EdgeCreateTraceFilterRuleResponses(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("span_attribute_rules",)
    span_attribute_rules = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeCreateSpanAttributeRulesResponse),
        graphql_name="spanAttributeRules",
    )


class EdgeCreateTraceObserverResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "trace_observer")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of("EdgeCreateTraceObserverResponseError"),
        graphql_name="errors",
    )

    trace_observer = sgqlc.types.Field(
        "EdgeTraceObserver", graphql_name="traceObserver"
    )


class EdgeCreateTraceObserverResponseError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeCreateTraceObserverResponseErrorType),
        graphql_name="type",
    )


class EdgeCreateTraceObserverResponses(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("responses",)
    responses = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(EdgeCreateTraceObserverResponse))
        ),
        graphql_name="responses",
    )


class EdgeDataSource(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entity", "status")
    entity = sgqlc.types.Field(EntityOutline, graphql_name="entity")

    status = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeDataSourceStatusType), graphql_name="status"
    )


class EdgeDataSourceGroup(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("data_sources",)
    data_sources = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EdgeDataSource))),
        graphql_name="dataSources",
    )


class EdgeDeleteSpanAttributeRuleResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "rule")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of("EdgeDeleteSpanAttributeRuleResponseError"),
        graphql_name="errors",
    )

    rule = sgqlc.types.Field("EdgeSpanAttributeRule", graphql_name="rule")


class EdgeDeleteSpanAttributeRuleResponseError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeDeleteSpanAttributeRuleResponseErrorType),
        graphql_name="type",
    )


class EdgeDeleteTraceFilterRuleResponses(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("span_attribute_rules",)
    span_attribute_rules = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(EdgeDeleteSpanAttributeRuleResponse)
            )
        ),
        graphql_name="spanAttributeRules",
    )


class EdgeDeleteTraceObserverResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "trace_observer")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of("EdgeDeleteTraceObserverResponseError"),
        graphql_name="errors",
    )

    trace_observer = sgqlc.types.Field(
        "EdgeTraceObserver", graphql_name="traceObserver"
    )


class EdgeDeleteTraceObserverResponseError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeDeleteTraceObserverResponseErrorType),
        graphql_name="type",
    )


class EdgeDeleteTraceObserverResponses(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("responses",)
    responses = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(EdgeDeleteTraceObserverResponse))
        ),
        graphql_name="responses",
    )


class EdgeEndpoint(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("agent", "endpoint_type", "https", "status")
    agent = sgqlc.types.Field(
        sgqlc.types.non_null("EdgeAgentEndpointDetail"), graphql_name="agent"
    )

    endpoint_type = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeEndpointType), graphql_name="endpointType"
    )

    https = sgqlc.types.Field(
        sgqlc.types.non_null("EdgeHttpsEndpointDetail"), graphql_name="https"
    )

    status = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeEndpointStatus), graphql_name="status"
    )


class EdgeRandomTraceFilter(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("percent_kept",)
    percent_kept = sgqlc.types.Field(
        sgqlc.types.non_null(Float), graphql_name="percentKept"
    )


class EdgeSpanAttributeRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("action", "id", "key", "key_operator", "value", "value_operator")
    action = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeTraceFilterAction), graphql_name="action"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    key_operator = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeSpanAttributeKeyOperator), graphql_name="keyOperator"
    )

    value = sgqlc.types.Field(String, graphql_name="value")

    value_operator = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeSpanAttributeValueOperator),
        graphql_name="valueOperator",
    )


class EdgeSpanAttributesTraceFilter(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("span_attribute_rules",)
    span_attribute_rules = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(EdgeSpanAttributeRule))
        ),
        graphql_name="spanAttributeRules",
    )


class EdgeTraceFilters(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("random_trace_filter", "span_attributes_trace_filter")
    random_trace_filter = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeRandomTraceFilter), graphql_name="randomTraceFilter"
    )

    span_attributes_trace_filter = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeSpanAttributesTraceFilter),
        graphql_name="spanAttributesTraceFilter",
    )


class EdgeTraceObserver(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "compliance_types",
        "data_source_group",
        "endpoints",
        "id",
        "monitoring_account_id",
        "name",
        "provider_region",
        "status",
        "trace_filters",
    )
    compliance_types = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(EdgeComplianceTypeCode)),
        graphql_name="complianceTypes",
    )

    data_source_group = sgqlc.types.Field(
        EdgeDataSourceGroup, graphql_name="dataSourceGroup"
    )

    endpoints = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EdgeEndpoint))),
        graphql_name="endpoints",
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    monitoring_account_id = sgqlc.types.Field(Int, graphql_name="monitoringAccountId")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    provider_region = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeProviderRegion), graphql_name="providerRegion"
    )

    status = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeTraceObserverStatus), graphql_name="status"
    )

    trace_filters = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeTraceFilters), graphql_name="traceFilters"
    )


class EdgeTracing(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("trace_observers",)
    trace_observers = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(EdgeTraceObserver)),
        graphql_name="traceObservers",
        args=sgqlc.types.ArgDict(
            (
                (
                    "ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(Int)),
                        graphql_name="ids",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `ids` (`[Int!]`)
    """


class EdgeUpdateTraceObserverResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "trace_observer")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of("EdgeUpdateTraceObserverResponseError"),
        graphql_name="errors",
    )

    trace_observer = sgqlc.types.Field(EdgeTraceObserver, graphql_name="traceObserver")


class EdgeUpdateTraceObserverResponseError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeUpdateTraceObserverResponseErrorType),
        graphql_name="type",
    )


class EdgeUpdateTraceObserverResponses(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("responses",)
    responses = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(EdgeUpdateTraceObserverResponse))
        ),
        graphql_name="responses",
    )


class EntityAlertViolation(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "agent_url",
        "alert_severity",
        "closed_at",
        "label",
        "level",
        "opened_at",
        "violation_id",
        "violation_url",
    )
    agent_url = sgqlc.types.Field(String, graphql_name="agentUrl")

    alert_severity = sgqlc.types.Field(
        EntityAlertSeverity, graphql_name="alertSeverity"
    )

    closed_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="closedAt")

    label = sgqlc.types.Field(String, graphql_name="label")

    level = sgqlc.types.Field(String, graphql_name="level")

    opened_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="openedAt")

    violation_id = sgqlc.types.Field(
        EntityAlertViolationInt, graphql_name="violationId"
    )

    violation_url = sgqlc.types.Field(String, graphql_name="violationUrl")


class EntityCollection(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account",
        "created_by",
        "definition",
        "guid",
        "members",
        "name",
        "type",
    )
    account = sgqlc.types.Field(AccountReference, graphql_name="account")

    created_by = sgqlc.types.Field("UserReference", graphql_name="createdBy")

    definition = sgqlc.types.Field(
        "EntityCollectionDefinition", graphql_name="definition"
    )

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    members = sgqlc.types.Field("EntitySearch", graphql_name="members")

    name = sgqlc.types.Field(String, graphql_name="name")

    type = sgqlc.types.Field(EntityCollectionType, graphql_name="type")


class EntityCollectionDefinition(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "entity_guids",
        "entity_search_query",
        "scope_accounts",
        "search_queries",
    )
    entity_guids = sgqlc.types.Field(
        sgqlc.types.list_of(EntityGuid), graphql_name="entityGuids"
    )

    entity_search_query = sgqlc.types.Field(String, graphql_name="entitySearchQuery")

    scope_accounts = sgqlc.types.Field(
        "EntityCollectionScopeAccounts", graphql_name="scopeAccounts"
    )

    search_queries = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="searchQueries"
    )


class EntityCollectionScopeAccounts(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_ids",)
    account_ids = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name="accountIds")


class EntityDeleteError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("guid", "message", "type")
    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(EntityDeleteErrorType), graphql_name="type"
    )


class EntityDeleteResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("deleted_entities", "failures")
    deleted_entities = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EntityGuid))),
        graphql_name="deletedEntities",
    )

    failures = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(EntityDeleteError))
        ),
        graphql_name="failures",
    )


class EntityGoldenContext(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account", "guid")
    account = sgqlc.types.Field(Int, graphql_name="account")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")


class EntityGoldenContextScopedGoldenMetrics(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("context", "metrics")
    context = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenContext), graphql_name="context"
    )

    metrics = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("EntityGoldenMetric"))
        ),
        graphql_name="metrics",
    )


class EntityGoldenContextScopedGoldenTags(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("context", "tags")
    context = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenContext), graphql_name="context"
    )

    tags = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("EntityGoldenTag"))
        ),
        graphql_name="tags",
    )


class EntityGoldenGoldenMetricsError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(String, graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenGoldenMetricsErrorType), graphql_name="type"
    )


class EntityGoldenMetric(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "definition",
        "metric_name",
        "name",
        "original_definitions",
        "original_queries",
        "query",
        "title",
        "unit",
    )
    definition = sgqlc.types.Field(
        sgqlc.types.non_null("EntityGoldenMetricDefinition"), graphql_name="definition"
    )

    metric_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="metricName"
    )

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    original_definitions = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null("EntityGoldenOriginalDefinitionWithSelector")
            )
        ),
        graphql_name="originalDefinitions",
    )

    original_queries = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null("EntityGoldenOriginalQueryWithSelector")
            )
        ),
        graphql_name="originalQueries",
    )

    query = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="query")

    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="title")

    unit = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenMetricUnit), graphql_name="unit"
    )


class EntityGoldenMetricDefinition(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "event_id",
        "event_object_id",
        "facet",
        "from_",
        "select",
        "where",
    )
    event_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="eventId")

    event_object_id = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenEventObjectId), graphql_name="eventObjectId"
    )

    facet = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="facet")

    from_ = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="from")

    select = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="select")

    where = sgqlc.types.Field(String, graphql_name="where")


class EntityGoldenMetricsDomainTypeScoped(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("context", "domain_type", "metrics")
    context = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenContext), graphql_name="context"
    )

    domain_type = sgqlc.types.Field(
        sgqlc.types.non_null(DomainType), graphql_name="domainType"
    )

    metrics = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(EntityGoldenMetric))
        ),
        graphql_name="metrics",
    )


class EntityGoldenMetricsDomainTypeScopedResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "metrics")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(EntityGoldenGoldenMetricsError)),
        graphql_name="errors",
    )

    metrics = sgqlc.types.Field(
        EntityGoldenMetricsDomainTypeScoped, graphql_name="metrics"
    )


class EntityGoldenOriginalDefinitionWithSelector(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("definition", "selector_value")
    definition = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenMetricDefinition), graphql_name="definition"
    )

    selector_value = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="selectorValue"
    )


class EntityGoldenOriginalQueryWithSelector(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("query", "selector_value")
    query = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="query")

    selector_value = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="selectorValue"
    )


class EntityGoldenTag(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("key",)
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")


class EntityGoldenTagsDomainTypeScoped(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("context", "domain_type", "tags")
    context = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenContext), graphql_name="context"
    )

    domain_type = sgqlc.types.Field(
        sgqlc.types.non_null(DomainType), graphql_name="domainType"
    )

    tags = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(EntityGoldenTag))
        ),
        graphql_name="tags",
    )


class EntityGoldenTagsDomainTypeScopedResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "tags")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(EntityGoldenGoldenMetricsError)),
        graphql_name="errors",
    )

    tags = sgqlc.types.Field(EntityGoldenTagsDomainTypeScoped, graphql_name="tags")


class EntityRelationship(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("type",)
    type = sgqlc.types.Field(EntityRelationshipType, graphql_name="type")


class EntityRelationshipNode(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entity",)
    entity = sgqlc.types.Field(EntityOutline, graphql_name="entity")


class EntityRelationshipRelatedEntitiesResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "results")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    results = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(EntityRelationshipEdge))
        ),
        graphql_name="results",
    )


class EntityRelationshipUserDefinedCreateOrReplaceResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(
                "EntityRelationshipUserDefinedCreateOrReplaceResultError"
            )
        ),
        graphql_name="errors",
    )


class EntityRelationshipUserDefinedCreateOrReplaceResultError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(EntityRelationshipUserDefinedCreateOrReplaceErrorType),
        graphql_name="type",
    )


class EntityRelationshipUserDefinedDeleteResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("EntityRelationshipUserDefinedDeleteResultError")
        ),
        graphql_name="errors",
    )


class EntityRelationshipUserDefinedDeleteResultError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(EntityRelationshipUserDefinedDeleteErrorType),
        graphql_name="type",
    )


class EntityRelationshipVertex(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "entity", "guid")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    entity = sgqlc.types.Field(EntityOutline, graphql_name="entity")

    guid = sgqlc.types.Field(sgqlc.types.non_null(EntityGuid), graphql_name="guid")


class EntitySearch(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "counts", "query", "results", "types")
    count = sgqlc.types.Field(Int, graphql_name="count")

    counts = sgqlc.types.Field(
        sgqlc.types.list_of("EntitySearchCounts"),
        graphql_name="counts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "facet",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(
                            sgqlc.types.non_null(EntitySearchCountsFacet)
                        ),
                        graphql_name="facet",
                        default=None,
                    ),
                ),
                (
                    "facet_tags",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(String)),
                        graphql_name="facetTags",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `facet` (`[EntitySearchCountsFacet!]`)
    * `facet_tags` (`[String!]`)
    """

    query = sgqlc.types.Field(String, graphql_name="query")

    results = sgqlc.types.Field(
        "EntitySearchResult",
        graphql_name="results",
        args=sgqlc.types.ArgDict(
            (("cursor", sgqlc.types.Arg(String, graphql_name="cursor", default=None)),)
        ),
    )

    types = sgqlc.types.Field(
        sgqlc.types.list_of("EntitySearchTypes"), graphql_name="types"
    )


class EntitySearchCounts(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "facet")
    count = sgqlc.types.Field(Int, graphql_name="count")

    facet = sgqlc.types.Field(AttributeMap, graphql_name="facet")


class EntitySearchResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entities", "next_cursor")
    entities = sgqlc.types.Field(
        sgqlc.types.list_of(EntityOutline), graphql_name="entities"
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")


class EntitySearchTypes(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "domain", "entity_type", "type")
    count = sgqlc.types.Field(Int, graphql_name="count")

    domain = sgqlc.types.Field(String, graphql_name="domain")

    entity_type = sgqlc.types.Field(EntityType, graphql_name="entityType")

    type = sgqlc.types.Field(String, graphql_name="type")


class EntityTag(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("key", "values")
    key = sgqlc.types.Field(String, graphql_name="key")

    values = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="values")


class EntityTagValueWithMetadata(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("mutable", "value")
    mutable = sgqlc.types.Field(Boolean, graphql_name="mutable")

    value = sgqlc.types.Field(String, graphql_name="value")


class EntityTagWithMetadata(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("key", "values")
    key = sgqlc.types.Field(String, graphql_name="key")

    values = sgqlc.types.Field(
        sgqlc.types.list_of(EntityTagValueWithMetadata), graphql_name="values"
    )


class ErrorsInboxActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error_group", "error_group_state_types", "error_groups")
    error_group = sgqlc.types.Field(
        "ErrorsInboxErrorGroup",
        graphql_name="errorGroup",
        args=sgqlc.types.ArgDict(
            (
                (
                    "error_event",
                    sgqlc.types.Arg(
                        ErrorsInboxErrorEventInput,
                        graphql_name="errorEvent",
                        default=None,
                    ),
                ),
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
            )
        ),
    )

    error_group_state_types = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("ErrorsInboxErrorGroupStateTypeResult")
        ),
        graphql_name="errorGroupStateTypes",
    )

    error_groups = sgqlc.types.Field(
        "ErrorsInboxErrorGroupsResponse",
        graphql_name="errorGroups",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "entity_guids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(EntityGuid)),
                        graphql_name="entityGuids",
                        default=None,
                    ),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        ErrorsInboxErrorGroupSearchFilterInput,
                        graphql_name="filter",
                        default=None,
                    ),
                ),
                ("query", sgqlc.types.Arg(String, graphql_name="query", default=None)),
                (
                    "sort_by",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(
                            sgqlc.types.non_null(ErrorsInboxErrorGroupSortOrderInput)
                        ),
                        graphql_name="sortBy",
                        default=None,
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `entity_guids` (`[EntityGuid!]`)
    * `filter` (`ErrorsInboxErrorGroupSearchFilterInput`)
    * `query` (`String`)
    * `sort_by` (`[ErrorsInboxErrorGroupSortOrderInput!]`)
    * `time_window` (`TimeWindowInput`)
    """


class ErrorsInboxAssignErrorGroupResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("assignment", "errors")
    assignment = sgqlc.types.Field("ErrorsInboxAssignment", graphql_name="assignment")

    errors = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("ErrorsInboxAssignErrorGroupError")),
        graphql_name="errors",
    )


class ErrorsInboxAssignment(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("email", "user_info")
    email = sgqlc.types.Field(String, graphql_name="email")

    user_info = sgqlc.types.Field("UserReference", graphql_name="userInfo")


class ErrorsInboxDeleteErrorGroupResourceResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("resource_id",)
    resource_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="resourceId")


class ErrorsInboxErrorGroup(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "assignment",
        "entity_guid",
        "events_query",
        "first_seen_at",
        "id",
        "last_seen_at",
        "message",
        "name",
        "occurrences",
        "regressed_at",
        "resources",
        "source",
        "state",
        "url",
    )
    assignment = sgqlc.types.Field(ErrorsInboxAssignment, graphql_name="assignment")

    entity_guid = sgqlc.types.Field(EntityGuid, graphql_name="entityGuid")

    events_query = sgqlc.types.Field(Nrql, graphql_name="eventsQuery")

    first_seen_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="firstSeenAt")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    last_seen_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="lastSeenAt")

    message = sgqlc.types.Field(String, graphql_name="message")

    name = sgqlc.types.Field(String, graphql_name="name")

    occurrences = sgqlc.types.Field(
        "ErrorsInboxOccurrences", graphql_name="occurrences"
    )

    regressed_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="regressedAt")

    resources = sgqlc.types.Field(
        sgqlc.types.non_null("ErrorsInboxResourcesResponse"),
        graphql_name="resources",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        ErrorsInboxResourceFilterInput,
                        graphql_name="filter",
                        default=None,
                    ),
                ),
            )
        ),
    )

    source = sgqlc.types.Field(String, graphql_name="source")

    state = sgqlc.types.Field(ErrorsInboxErrorGroupState, graphql_name="state")

    url = sgqlc.types.Field(String, graphql_name="url")


class ErrorsInboxErrorGroupStateTypeResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("type",)
    type = sgqlc.types.Field(ErrorsInboxErrorGroupState, graphql_name="type")


class ErrorsInboxErrorGroupsResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "results", "total_count")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    results = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(ErrorsInboxErrorGroup)),
        graphql_name="results",
    )

    total_count = sgqlc.types.Field(Int, graphql_name="totalCount")


class ErrorsInboxOccurrences(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("expected_count", "first_seen_at", "last_seen_at", "total_count")
    expected_count = sgqlc.types.Field(Int, graphql_name="expectedCount")

    first_seen_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="firstSeenAt")

    last_seen_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="lastSeenAt")

    total_count = sgqlc.types.Field(Int, graphql_name="totalCount")


class ErrorsInboxResourcesResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "results", "total_count")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    results = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(ErrorsInboxResource))
        ),
        graphql_name="results",
    )

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class ErrorsInboxUpdateErrorGroupStateResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("state",)
    state = sgqlc.types.Field(ErrorsInboxErrorGroupState, graphql_name="state")


class EventAttributeDefinition(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("definition", "documentation_url", "label", "name")
    definition = sgqlc.types.Field(String, graphql_name="definition")

    documentation_url = sgqlc.types.Field(String, graphql_name="documentationUrl")

    label = sgqlc.types.Field(String, graphql_name="label")

    name = sgqlc.types.Field(String, graphql_name="name")


class EventDefinition(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attributes", "definition", "label", "name")
    attributes = sgqlc.types.Field(
        sgqlc.types.list_of(EventAttributeDefinition), graphql_name="attributes"
    )

    definition = sgqlc.types.Field(String, graphql_name="definition")

    label = sgqlc.types.Field(String, graphql_name="label")

    name = sgqlc.types.Field(String, graphql_name="name")


class EventsToMetricsAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("all_rules", "rules_by_id")
    all_rules = sgqlc.types.Field(
        "EventsToMetricsListRuleResult", graphql_name="allRules"
    )

    rules_by_id = sgqlc.types.Field(
        "EventsToMetricsListRuleResult",
        graphql_name="rulesById",
        args=sgqlc.types.ArgDict(
            (
                (
                    "rule_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(ID)),
                        graphql_name="ruleIds",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `rule_ids` (`[ID]!`)
    """


class EventsToMetricsCreateRuleFailure(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "submitted")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of("EventsToMetricsError"), graphql_name="errors"
    )

    submitted = sgqlc.types.Field(
        "EventsToMetricsCreateRuleSubmission", graphql_name="submitted"
    )


class EventsToMetricsCreateRuleResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("failures", "successes")
    failures = sgqlc.types.Field(
        sgqlc.types.list_of(EventsToMetricsCreateRuleFailure), graphql_name="failures"
    )

    successes = sgqlc.types.Field(
        sgqlc.types.list_of("EventsToMetricsRule"), graphql_name="successes"
    )


class EventsToMetricsCreateRuleSubmission(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "description", "name", "nrql")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    description = sgqlc.types.Field(String, graphql_name="description")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    nrql = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="nrql")


class EventsToMetricsDeleteRuleFailure(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "submitted")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of("EventsToMetricsError"), graphql_name="errors"
    )

    submitted = sgqlc.types.Field(
        "EventsToMetricsDeleteRuleSubmission", graphql_name="submitted"
    )


class EventsToMetricsDeleteRuleResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("failures", "successes")
    failures = sgqlc.types.Field(
        sgqlc.types.list_of(EventsToMetricsDeleteRuleFailure), graphql_name="failures"
    )

    successes = sgqlc.types.Field(
        sgqlc.types.list_of("EventsToMetricsRule"), graphql_name="successes"
    )


class EventsToMetricsDeleteRuleSubmission(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "rule_id")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    rule_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="ruleId")


class EventsToMetricsError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "reason")
    description = sgqlc.types.Field(String, graphql_name="description")

    reason = sgqlc.types.Field(EventsToMetricsErrorReason, graphql_name="reason")


class EventsToMetricsListRuleResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("rules",)
    rules = sgqlc.types.Field(
        sgqlc.types.list_of("EventsToMetricsRule"), graphql_name="rules"
    )


class EventsToMetricsRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "created_at",
        "description",
        "enabled",
        "id",
        "name",
        "nrql",
        "updated_at",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    nrql = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="nrql")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )


class EventsToMetricsUpdateRuleFailure(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "submitted")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(EventsToMetricsError), graphql_name="errors"
    )

    submitted = sgqlc.types.Field(
        "EventsToMetricsUpdateRuleSubmission", graphql_name="submitted"
    )


class EventsToMetricsUpdateRuleResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("failures", "successes")
    failures = sgqlc.types.Field(
        sgqlc.types.list_of(EventsToMetricsUpdateRuleFailure), graphql_name="failures"
    )

    successes = sgqlc.types.Field(
        sgqlc.types.list_of(EventsToMetricsRule), graphql_name="successes"
    )


class EventsToMetricsUpdateRuleSubmission(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "enabled", "rule_id")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    rule_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="ruleId")


class HistoricalDataExportAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("export", "exports")
    export = sgqlc.types.Field(
        "HistoricalDataExportCustomerExportResponse",
        graphql_name="export",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    exports = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("HistoricalDataExportCustomerExportResponse")
        ),
        graphql_name="exports",
    )


class HistoricalDataExportCustomerExportResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account",
        "available_until",
        "begin_time",
        "created_at",
        "end_time",
        "event_count",
        "event_types",
        "id",
        "message",
        "nrql",
        "percent_complete",
        "results",
        "status",
        "user",
    )
    account = sgqlc.types.Field(AccountReference, graphql_name="account")

    available_until = sgqlc.types.Field(
        EpochMilliseconds, graphql_name="availableUntil"
    )

    begin_time = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="beginTime"
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    end_time = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="endTime"
    )

    event_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="eventCount"
    )

    event_types = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="eventTypes",
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    message = sgqlc.types.Field(String, graphql_name="message")

    nrql = sgqlc.types.Field(sgqlc.types.non_null(Nrql), graphql_name="nrql")

    percent_complete = sgqlc.types.Field(
        sgqlc.types.non_null(Float), graphql_name="percentComplete"
    )

    results = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="results")

    status = sgqlc.types.Field(
        sgqlc.types.non_null(HistoricalDataExportStatus), graphql_name="status"
    )

    user = sgqlc.types.Field("UserReference", graphql_name="user")


class IncidentIntelligenceEnvironmentAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("current_environment",)
    current_environment = sgqlc.types.Field(
        "IncidentIntelligenceEnvironmentCurrentEnvironmentResult",
        graphql_name="currentEnvironment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "kind",
                    sgqlc.types.Arg(
                        IncidentIntelligenceEnvironmentSupportedEnvironmentKind,
                        graphql_name="kind",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `kind`
      (`IncidentIntelligenceEnvironmentSupportedEnvironmentKind`)
    """


class IncidentIntelligenceEnvironmentActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "authorized_environments",
        "consented_accounts",
        "current_environment",
    )
    authorized_environments = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(
                "IncidentIntelligenceEnvironmentIncidentIntelligenceEnvironment"
            )
        ),
        graphql_name="authorizedEnvironments",
        args=sgqlc.types.ArgDict(
            (
                (
                    "kind",
                    sgqlc.types.Arg(
                        IncidentIntelligenceEnvironmentSupportedEnvironmentKind,
                        graphql_name="kind",
                        default=None,
                    ),
                ),
            )
        ),
    )

    consented_accounts = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("IncidentIntelligenceEnvironmentConsentedAccount")
        ),
        graphql_name="consentedAccounts",
    )

    current_environment = sgqlc.types.Field(
        "IncidentIntelligenceEnvironmentCurrentEnvironmentResult",
        graphql_name="currentEnvironment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "kind",
                    sgqlc.types.Arg(
                        IncidentIntelligenceEnvironmentSupportedEnvironmentKind,
                        graphql_name="kind",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `kind`
      (`IncidentIntelligenceEnvironmentSupportedEnvironmentKind`)
    """


class IncidentIntelligenceEnvironmentConsentAccounts(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("consented_accounts", "result")
    consented_accounts = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("IncidentIntelligenceEnvironmentConsentedAccount")
        ),
        graphql_name="consentedAccounts",
    )

    result = sgqlc.types.Field(
        sgqlc.types.non_null(IncidentIntelligenceEnvironmentConsentAccountsResult),
        graphql_name="result",
    )


class IncidentIntelligenceEnvironmentConsentAuthorizedAccounts(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("consented_accounts", "result")
    consented_accounts = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("IncidentIntelligenceEnvironmentConsentedAccount")
        ),
        graphql_name="consentedAccounts",
    )

    result = sgqlc.types.Field(
        sgqlc.types.non_null(IncidentIntelligenceEnvironmentConsentAccountsResult),
        graphql_name="result",
    )


class IncidentIntelligenceEnvironmentConsentedAccount(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account",)
    account = sgqlc.types.Field(AccountReference, graphql_name="account")


class IncidentIntelligenceEnvironmentCreateEnvironment(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("result", "result_details")
    result = sgqlc.types.Field(
        sgqlc.types.non_null(IncidentIntelligenceEnvironmentCreateEnvironmentResult),
        graphql_name="result",
    )

    result_details = sgqlc.types.Field(
        "IncidentIntelligenceEnvironmentCreateEnvironmentResultDetails",
        graphql_name="resultDetails",
    )


class IncidentIntelligenceEnvironmentCurrentEnvironmentResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("environment", "reason", "reason_details")
    environment = sgqlc.types.Field(
        "IncidentIntelligenceEnvironmentIncidentIntelligenceEnvironment",
        graphql_name="environment",
    )

    reason = sgqlc.types.Field(
        IncidentIntelligenceEnvironmentCurrentEnvironmentResultReason,
        graphql_name="reason",
    )

    reason_details = sgqlc.types.Field(
        "IncidentIntelligenceEnvironmentCurrentEnvironmentResultReasonDetails",
        graphql_name="reasonDetails",
    )


class IncidentIntelligenceEnvironmentDeleteEnvironment(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("result",)
    result = sgqlc.types.Field(
        sgqlc.types.non_null(IncidentIntelligenceEnvironmentDeleteEnvironmentResult),
        graphql_name="result",
    )


class IncidentIntelligenceEnvironmentDissentAccounts(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("dissented_accounts", "result")
    dissented_accounts = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(IncidentIntelligenceEnvironmentConsentedAccount)
        ),
        graphql_name="dissentedAccounts",
    )

    result = sgqlc.types.Field(
        sgqlc.types.non_null(IncidentIntelligenceEnvironmentDissentAccountsResult),
        graphql_name="result",
    )


class IncidentIntelligenceEnvironmentEnvironmentAlreadyExists(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "environment", "master_account_id")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    environment = sgqlc.types.Field(
        sgqlc.types.non_null(
            "IncidentIntelligenceEnvironmentIncidentIntelligenceEnvironment"
        ),
        graphql_name="environment",
    )

    master_account_id = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="masterAccountId"
    )


class IncidentIntelligenceEnvironmentEnvironmentCreated(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("environment",)
    environment = sgqlc.types.Field(
        sgqlc.types.non_null(
            "IncidentIntelligenceEnvironmentIncidentIntelligenceEnvironment"
        ),
        graphql_name="environment",
    )


class IncidentIntelligenceEnvironmentIncidentIntelligenceEnvironment(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "associated_authorized_accounts",
        "billing_cycle_quota",
        "created_at",
        "created_by",
        "incident_intelligence_account",
        "is_consent_required",
        "is_entitled_for_ai",
        "is_free_tier",
        "kind",
        "master_account",
        "name",
        "was_consented",
    )
    associated_authorized_accounts = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(AccountReference)),
        graphql_name="associatedAuthorizedAccounts",
    )

    billing_cycle_quota = sgqlc.types.Field(Int, graphql_name="billingCycleQuota")

    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    created_by = sgqlc.types.Field("UserReference", graphql_name="createdBy")

    incident_intelligence_account = sgqlc.types.Field(
        AccountReference, graphql_name="incidentIntelligenceAccount"
    )

    is_consent_required = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="isConsentRequired"
    )

    is_entitled_for_ai = sgqlc.types.Field(Boolean, graphql_name="isEntitledForAi")

    is_free_tier = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="isFreeTier"
    )

    kind = sgqlc.types.Field(
        IncidentIntelligenceEnvironmentEnvironmentKind, graphql_name="kind"
    )

    master_account = sgqlc.types.Field(AccountReference, graphql_name="masterAccount")

    name = sgqlc.types.Field(String, graphql_name="name")

    was_consented = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="wasConsented"
    )


class IncidentIntelligenceEnvironmentMultipleEnvironmentsAvailable(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_ids",)
    account_ids = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name="accountIds")


class IncidentIntelligenceEnvironmentUserNotAuthorizedForAccount(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id",)
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")


class IncidentIntelligenceEnvironmentUserNotCapableToOperateOnAccount(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "capability")
    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    capability = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="capability"
    )


class InfrastructureHostSummaryData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "cpu_utilization_percent",
        "disk_used_percent",
        "memory_used_percent",
        "network_receive_rate",
        "network_transmit_rate",
        "services_count",
    )
    cpu_utilization_percent = sgqlc.types.Field(
        Float, graphql_name="cpuUtilizationPercent"
    )

    disk_used_percent = sgqlc.types.Field(Float, graphql_name="diskUsedPercent")

    memory_used_percent = sgqlc.types.Field(Float, graphql_name="memoryUsedPercent")

    network_receive_rate = sgqlc.types.Field(Float, graphql_name="networkReceiveRate")

    network_transmit_rate = sgqlc.types.Field(Float, graphql_name="networkTransmitRate")

    services_count = sgqlc.types.Field(Int, graphql_name="servicesCount")


class InstallationAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("install_status", "recipe_events", "recipes", "statuses")
    install_status = sgqlc.types.Field(
        "InstallationInstallStatus", graphql_name="installStatus"
    )

    recipe_events = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("InstallationRecipeEvent")),
        graphql_name="recipeEvents",
    )

    recipes = sgqlc.types.Field(
        "InstallationRecipeEventResult",
        graphql_name="recipes",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "install_id",
                    sgqlc.types.Arg(String, graphql_name="installId", default=None),
                ),
            )
        ),
    )

    statuses = sgqlc.types.Field(
        "InstallationInstallStatusResult",
        graphql_name="statuses",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "install_id",
                    sgqlc.types.Arg(String, graphql_name="installId", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `install_id` (`String`)
    """


class InstallationInstallStatus(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "cli_version",
        "deployed_by",
        "enabled_proxy",
        "error",
        "host_name",
        "install_id",
        "install_library_version",
        "is_unsupported",
        "kernel_arch",
        "kernel_version",
        "log_file_path",
        "os",
        "platform",
        "platform_family",
        "platform_version",
        "redirect_url",
        "state",
        "targeted_install",
        "timestamp",
    )
    cli_version = sgqlc.types.Field(
        sgqlc.types.non_null(SemVer), graphql_name="cliVersion"
    )

    deployed_by = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="deployedBy"
    )

    enabled_proxy = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="enabledProxy"
    )

    error = sgqlc.types.Field(
        sgqlc.types.non_null("InstallationStatusError"), graphql_name="error"
    )

    host_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="hostName")

    install_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="installId")

    install_library_version = sgqlc.types.Field(
        sgqlc.types.non_null(SemVer), graphql_name="installLibraryVersion"
    )

    is_unsupported = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="isUnsupported"
    )

    kernel_arch = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="kernelArch"
    )

    kernel_version = sgqlc.types.Field(
        sgqlc.types.non_null(SemVer), graphql_name="kernelVersion"
    )

    log_file_path = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="logFilePath"
    )

    os = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="os")

    platform = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="platform")

    platform_family = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="platformFamily"
    )

    platform_version = sgqlc.types.Field(
        sgqlc.types.non_null(SemVer), graphql_name="platformVersion"
    )

    redirect_url = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="redirectUrl"
    )

    state = sgqlc.types.Field(
        sgqlc.types.non_null(InstallationInstallStateType), graphql_name="state"
    )

    targeted_install = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="targetedInstall"
    )

    timestamp = sgqlc.types.Field(EpochSeconds, graphql_name="timestamp")


class InstallationInstallStatusResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("cursor", "install_statuses", "total_count")
    cursor = sgqlc.types.Field(String, graphql_name="cursor")

    install_statuses = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(InstallationInstallStatus)),
        graphql_name="installStatuses",
    )

    total_count = sgqlc.types.Field(Int, graphql_name="totalCount")


class InstallationRecipeEvent(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "cli_version",
        "complete",
        "display_name",
        "entity_guid",
        "error",
        "host_name",
        "install_id",
        "install_library_version",
        "kernel_arch",
        "kernel_version",
        "log_file_path",
        "metadata",
        "name",
        "os",
        "platform",
        "platform_family",
        "platform_version",
        "redirect_url",
        "status",
        "targeted_install",
        "task_path",
        "timestamp",
        "validation_duration_milliseconds",
    )
    cli_version = sgqlc.types.Field(
        sgqlc.types.non_null(SemVer), graphql_name="cliVersion"
    )

    complete = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="complete")

    display_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="displayName"
    )

    entity_guid = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGuid), graphql_name="entityGuid"
    )

    error = sgqlc.types.Field(
        sgqlc.types.non_null("InstallationStatusError"), graphql_name="error"
    )

    host_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="hostName")

    install_id = sgqlc.types.Field(ID, graphql_name="installId")

    install_library_version = sgqlc.types.Field(
        SemVer, graphql_name="installLibraryVersion"
    )

    kernel_arch = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="kernelArch"
    )

    kernel_version = sgqlc.types.Field(
        sgqlc.types.non_null(SemVer), graphql_name="kernelVersion"
    )

    log_file_path = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="logFilePath"
    )

    metadata = sgqlc.types.Field(InstallationRawMetadata, graphql_name="metadata")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    os = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="os")

    platform = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="platform")

    platform_family = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="platformFamily"
    )

    platform_version = sgqlc.types.Field(
        sgqlc.types.non_null(SemVer), graphql_name="platformVersion"
    )

    redirect_url = sgqlc.types.Field(String, graphql_name="redirectUrl")

    status = sgqlc.types.Field(
        sgqlc.types.non_null(InstallationRecipeStatusType), graphql_name="status"
    )

    targeted_install = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="targetedInstall"
    )

    task_path = sgqlc.types.Field(String, graphql_name="taskPath")

    timestamp = sgqlc.types.Field(
        sgqlc.types.non_null(EpochSeconds), graphql_name="timestamp"
    )

    validation_duration_milliseconds = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds),
        graphql_name="validationDurationMilliseconds",
    )


class InstallationRecipeEventResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("cursor", "recipe_events", "total_count")
    cursor = sgqlc.types.Field(String, graphql_name="cursor")

    recipe_events = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(InstallationRecipeEvent)),
        graphql_name="recipeEvents",
    )

    total_count = sgqlc.types.Field(Int, graphql_name="totalCount")


class InstallationStatusError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("details", "message")
    details = sgqlc.types.Field(String, graphql_name="details")

    message = sgqlc.types.Field(String, graphql_name="message")


class JavaFlightRecorderFlamegraph(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("all_frames",)
    all_frames = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of("JavaFlightRecorderStackFrame")),
        graphql_name="allFrames",
    )


class JavaFlightRecorderStackFrame(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "id", "name", "parent_id")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    parent_id = sgqlc.types.Field(ID, graphql_name="parentId")


class KeyTransactionApplication(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entity", "guid")
    entity = sgqlc.types.Field(EntityOutline, graphql_name="entity")

    guid = sgqlc.types.Field(sgqlc.types.non_null(EntityGuid), graphql_name="guid")


class KeyTransactionCreateResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "apdex_target",
        "application",
        "browser_apdex_target",
        "guid",
        "metric_name",
        "name",
    )
    apdex_target = sgqlc.types.Field(Float, graphql_name="apdexTarget")

    application = sgqlc.types.Field(
        sgqlc.types.non_null(KeyTransactionApplication), graphql_name="application"
    )

    browser_apdex_target = sgqlc.types.Field(Float, graphql_name="browserApdexTarget")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    metric_name = sgqlc.types.Field(String, graphql_name="metricName")

    name = sgqlc.types.Field(String, graphql_name="name")


class KeyTransactionDeleteResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("success",)
    success = sgqlc.types.Field(Boolean, graphql_name="success")


class KeyTransactionUpdateResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("apdex_target", "application", "browser_apdex_target", "name")
    apdex_target = sgqlc.types.Field(Float, graphql_name="apdexTarget")

    application = sgqlc.types.Field(
        sgqlc.types.non_null(KeyTransactionApplication), graphql_name="application"
    )

    browser_apdex_target = sgqlc.types.Field(Float, graphql_name="browserApdexTarget")

    name = sgqlc.types.Field(String, graphql_name="name")


class LogConfigurationsAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "data_partition_rules",
        "obfuscation_expressions",
        "obfuscation_rules",
        "parsing_rules",
        "pipeline_configuration",
        "test_grok",
    )
    data_partition_rules = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("LogConfigurationsDataPartitionRule")),
        graphql_name="dataPartitionRules",
    )

    obfuscation_expressions = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null("LogConfigurationsObfuscationExpression")
        ),
        graphql_name="obfuscationExpressions",
    )

    obfuscation_rules = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("LogConfigurationsObfuscationRule")),
        graphql_name="obfuscationRules",
    )

    parsing_rules = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("LogConfigurationsParsingRule")),
        graphql_name="parsingRules",
    )

    pipeline_configuration = sgqlc.types.Field(
        "LogConfigurationsPipelineConfiguration", graphql_name="pipelineConfiguration"
    )

    test_grok = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("LogConfigurationsGrokTestResult")),
        graphql_name="testGrok",
        args=sgqlc.types.ArgDict(
            (
                (
                    "grok",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="grok", default=None
                    ),
                ),
                (
                    "log_lines",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(String))
                        ),
                        graphql_name="logLines",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `grok` (`String!`)
    * `log_lines` (`[String!]!`)
    """


class LogConfigurationsCreateDataPartitionRuleError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(String, graphql_name="message")

    type = sgqlc.types.Field(
        LogConfigurationsCreateDataPartitionRuleErrorType, graphql_name="type"
    )


class LogConfigurationsCreateDataPartitionRuleResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "rule")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(LogConfigurationsCreateDataPartitionRuleError),
        graphql_name="errors",
    )

    rule = sgqlc.types.Field("LogConfigurationsDataPartitionRule", graphql_name="rule")


class LogConfigurationsCreateParsingRuleResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "rule")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of("LogConfigurationsParsingRuleMutationError"),
        graphql_name="errors",
    )

    rule = sgqlc.types.Field("LogConfigurationsParsingRule", graphql_name="rule")


class LogConfigurationsDataPartitionRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "created_by",
        "deleted",
        "description",
        "enabled",
        "id",
        "nrql",
        "retention_policy",
        "target_data_partition",
        "updated_at",
        "updated_by",
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    created_by = sgqlc.types.Field("UserReference", graphql_name="createdBy")

    deleted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="deleted")

    description = sgqlc.types.Field(String, graphql_name="description")

    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    nrql = sgqlc.types.Field(Nrql, graphql_name="nrql")

    retention_policy = sgqlc.types.Field(
        sgqlc.types.non_null(LogConfigurationsDataPartitionRuleRetentionPolicyType),
        graphql_name="retentionPolicy",
    )

    target_data_partition = sgqlc.types.Field(
        sgqlc.types.non_null(LogConfigurationsLogDataPartitionName),
        graphql_name="targetDataPartition",
    )

    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")

    updated_by = sgqlc.types.Field("UserReference", graphql_name="updatedBy")


class LogConfigurationsDataPartitionRuleMatchingCriteria(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attribute_name", "matching_expression", "matching_operator")
    attribute_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="attributeName"
    )

    matching_expression = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="matchingExpression"
    )

    matching_operator = sgqlc.types.Field(
        sgqlc.types.non_null(LogConfigurationsDataPartitionRuleMatchingOperator),
        graphql_name="matchingOperator",
    )


class LogConfigurationsDataPartitionRuleMutationError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(String, graphql_name="message")

    type = sgqlc.types.Field(
        LogConfigurationsDataPartitionRuleMutationErrorType, graphql_name="type"
    )


class LogConfigurationsDeleteDataPartitionRuleResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(LogConfigurationsDataPartitionRuleMutationError),
        graphql_name="errors",
    )


class LogConfigurationsDeleteParsingRuleResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of("LogConfigurationsParsingRuleMutationError"),
        graphql_name="errors",
    )


class LogConfigurationsGrokTestExtractedAttribute(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class LogConfigurationsGrokTestResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attributes", "log_line", "matched")
    attributes = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(LogConfigurationsGrokTestExtractedAttribute)
        ),
        graphql_name="attributes",
    )

    log_line = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="logLine")

    matched = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="matched")


class LogConfigurationsObfuscationAction(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attributes", "expression", "id", "method")
    attributes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="attributes",
    )

    expression = sgqlc.types.Field(
        sgqlc.types.non_null("LogConfigurationsObfuscationExpression"),
        graphql_name="expression",
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    method = sgqlc.types.Field(
        sgqlc.types.non_null(LogConfigurationsObfuscationMethod), graphql_name="method"
    )


class LogConfigurationsObfuscationExpression(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "created_by",
        "description",
        "id",
        "name",
        "regex",
        "updated_at",
        "updated_by",
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    created_by = sgqlc.types.Field("UserReference", graphql_name="createdBy")

    description = sgqlc.types.Field(String, graphql_name="description")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    regex = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="regex")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )

    updated_by = sgqlc.types.Field("UserReference", graphql_name="updatedBy")


class LogConfigurationsObfuscationRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "actions",
        "created_at",
        "created_by",
        "description",
        "enabled",
        "filter",
        "id",
        "name",
        "updated_at",
        "updated_by",
    )
    actions = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(LogConfigurationsObfuscationAction)),
        graphql_name="actions",
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    created_by = sgqlc.types.Field("UserReference", graphql_name="createdBy")

    description = sgqlc.types.Field(String, graphql_name="description")

    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    filter = sgqlc.types.Field(sgqlc.types.non_null(Nrql), graphql_name="filter")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )

    updated_by = sgqlc.types.Field("UserReference", graphql_name="updatedBy")


class LogConfigurationsParsingRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "attribute",
        "created_by",
        "deleted",
        "description",
        "enabled",
        "grok",
        "id",
        "lucene",
        "nrql",
        "updated_at",
        "updated_by",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    attribute = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="attribute"
    )

    created_by = sgqlc.types.Field("UserReference", graphql_name="createdBy")

    deleted = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="deleted")

    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    grok = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="grok")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    lucene = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="lucene")

    nrql = sgqlc.types.Field(sgqlc.types.non_null(Nrql), graphql_name="nrql")

    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")

    updated_by = sgqlc.types.Field("UserReference", graphql_name="updatedBy")


class LogConfigurationsParsingRuleMutationError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(String, graphql_name="message")

    type = sgqlc.types.Field(
        LogConfigurationsParsingRuleMutationErrorType, graphql_name="type"
    )


class LogConfigurationsPipelineConfiguration(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "enrichment_disabled",
        "json_parsing_disabled",
        "obfuscation_disabled",
        "parsing_disabled",
        "patterns_enabled",
        "recursive_json_parsing_disabled",
        "transformation_disabled",
        "updated_at",
        "updated_by",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    enrichment_disabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="enrichmentDisabled"
    )

    json_parsing_disabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="jsonParsingDisabled"
    )

    obfuscation_disabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="obfuscationDisabled"
    )

    parsing_disabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="parsingDisabled"
    )

    patterns_enabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="patternsEnabled"
    )

    recursive_json_parsing_disabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="recursiveJsonParsingDisabled"
    )

    transformation_disabled = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="transformationDisabled"
    )

    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")

    updated_by = sgqlc.types.Field("UserReference", graphql_name="updatedBy")


class LogConfigurationsUpdateDataPartitionRuleResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "rule")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(LogConfigurationsDataPartitionRuleMutationError),
        graphql_name="errors",
    )

    rule = sgqlc.types.Field(LogConfigurationsDataPartitionRule, graphql_name="rule")


class LogConfigurationsUpdateParsingRuleResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "rule")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(LogConfigurationsParsingRuleMutationError),
        graphql_name="errors",
    )

    rule = sgqlc.types.Field(LogConfigurationsParsingRule, graphql_name="rule")


class LogConfigurationsUpsertPipelineConfigurationResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("pipeline_configuration",)
    pipeline_configuration = sgqlc.types.Field(
        LogConfigurationsPipelineConfiguration, graphql_name="pipelineConfiguration"
    )


class MetricNormalizationAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("metric_normalization_rule", "metric_normalization_rules")
    metric_normalization_rule = sgqlc.types.Field(
        "MetricNormalizationRule",
        graphql_name="metricNormalizationRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    metric_normalization_rules = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("MetricNormalizationRule")),
        graphql_name="metricNormalizationRules",
        args=sgqlc.types.ArgDict(
            (
                (
                    "enabled",
                    sgqlc.types.Arg(Boolean, graphql_name="enabled", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `enabled` (`Boolean`)
    """


class MetricNormalizationRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "action",
        "application_guid",
        "application_name",
        "created_at",
        "enabled",
        "eval_order",
        "id",
        "match_expression",
        "notes",
        "replacement",
        "terminate_chain",
    )
    action = sgqlc.types.Field(MetricNormalizationRuleAction, graphql_name="action")

    application_guid = sgqlc.types.Field(EntityGuid, graphql_name="applicationGuid")

    application_name = sgqlc.types.Field(String, graphql_name="applicationName")

    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    eval_order = sgqlc.types.Field(Int, graphql_name="evalOrder")

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    match_expression = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="matchExpression"
    )

    notes = sgqlc.types.Field(String, graphql_name="notes")

    replacement = sgqlc.types.Field(String, graphql_name="replacement")

    terminate_chain = sgqlc.types.Field(Boolean, graphql_name="terminateChain")


class MetricNormalizationRuleMetricGroupingIssue(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "denied_metrics_count",
        "denied_metrics_rate_per_minute",
        "metric_normalization_rule_id",
        "mitigated",
        "mitigation_rate_threshold",
        "mitigation_rate_window_size",
    )
    denied_metrics_count = sgqlc.types.Field(Int, graphql_name="deniedMetricsCount")

    denied_metrics_rate_per_minute = sgqlc.types.Field(
        Float, graphql_name="deniedMetricsRatePerMinute"
    )

    metric_normalization_rule_id = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="metricNormalizationRuleId"
    )

    mitigated = sgqlc.types.Field(Boolean, graphql_name="mitigated")

    mitigation_rate_threshold = sgqlc.types.Field(
        Float, graphql_name="mitigationRateThreshold"
    )

    mitigation_rate_window_size = sgqlc.types.Field(
        Int, graphql_name="mitigationRateWindowSize"
    )


class MetricNormalizationRuleMutationError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(String, graphql_name="message")

    type = sgqlc.types.Field(MetricNormalizationRuleErrorType, graphql_name="type")


class MetricNormalizationRuleMutationResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "rule")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(MetricNormalizationRuleMutationError), graphql_name="errors"
    )

    rule = sgqlc.types.Field(MetricNormalizationRule, graphql_name="rule")


class MobileAppSummaryData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "app_launch_count",
        "crash_count",
        "crash_rate",
        "http_error_rate",
        "http_request_count",
        "http_request_rate",
        "http_response_time_average",
        "mobile_session_count",
        "network_failure_rate",
        "users_affected_count",
    )
    app_launch_count = sgqlc.types.Field(Int, graphql_name="appLaunchCount")

    crash_count = sgqlc.types.Field(Int, graphql_name="crashCount")

    crash_rate = sgqlc.types.Field(Float, graphql_name="crashRate")

    http_error_rate = sgqlc.types.Field(Float, graphql_name="httpErrorRate")

    http_request_count = sgqlc.types.Field(Int, graphql_name="httpRequestCount")

    http_request_rate = sgqlc.types.Field(Float, graphql_name="httpRequestRate")

    http_response_time_average = sgqlc.types.Field(
        Seconds, graphql_name="httpResponseTimeAverage"
    )

    mobile_session_count = sgqlc.types.Field(Int, graphql_name="mobileSessionCount")

    network_failure_rate = sgqlc.types.Field(Float, graphql_name="networkFailureRate")

    users_affected_count = sgqlc.types.Field(Int, graphql_name="usersAffectedCount")


class MobilePushNotificationActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("devices",)
    devices = sgqlc.types.Field(
        sgqlc.types.list_of("MobilePushNotificationDevice"), graphql_name="devices"
    )


class MobilePushNotificationDevice(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "app_version",
        "device_id",
        "device_name",
        "operating_system",
        "user_id",
    )
    app_version = sgqlc.types.Field(
        sgqlc.types.non_null(SemVer), graphql_name="appVersion"
    )

    device_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="deviceId")

    device_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="deviceName"
    )

    operating_system = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="operatingSystem"
    )

    user_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="userId")


class MobilePushNotificationRemoveDeviceResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("device_id", "message")
    device_id = sgqlc.types.Field(String, graphql_name="deviceId")

    message = sgqlc.types.Field(String, graphql_name="message")


class MobilePushNotificationSendPushResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message",)
    message = sgqlc.types.Field(String, graphql_name="message")


class NerdStorageAccountScope(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("collection", "document")
    collection = sgqlc.types.Field(
        sgqlc.types.list_of("NerdStorageCollectionMember"),
        graphql_name="collection",
        args=sgqlc.types.ArgDict(
            (
                (
                    "collection",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="collection",
                        default=None,
                    ),
                ),
            )
        ),
    )

    document = sgqlc.types.Field(
        NerdStorageDocument,
        graphql_name="document",
        args=sgqlc.types.ArgDict(
            (
                (
                    "collection",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="collection",
                        default=None,
                    ),
                ),
                (
                    "document_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="documentId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `collection` (`String!`)
    * `document_id` (`String!`)
    """


class NerdStorageActorScope(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("collection", "document")
    collection = sgqlc.types.Field(
        sgqlc.types.list_of("NerdStorageCollectionMember"),
        graphql_name="collection",
        args=sgqlc.types.ArgDict(
            (
                (
                    "collection",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="collection",
                        default=None,
                    ),
                ),
            )
        ),
    )

    document = sgqlc.types.Field(
        NerdStorageDocument,
        graphql_name="document",
        args=sgqlc.types.ArgDict(
            (
                (
                    "collection",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="collection",
                        default=None,
                    ),
                ),
                (
                    "document_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="documentId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `collection` (`String!`)
    * `document_id` (`String!`)
    """


class NerdStorageCollectionMember(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("document", "id")
    document = sgqlc.types.Field(NerdStorageDocument, graphql_name="document")

    id = sgqlc.types.Field(String, graphql_name="id")


class NerdStorageDeleteResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("deleted",)
    deleted = sgqlc.types.Field(Int, graphql_name="deleted")


class NerdStorageEntityScope(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("collection", "document")
    collection = sgqlc.types.Field(
        sgqlc.types.list_of(NerdStorageCollectionMember),
        graphql_name="collection",
        args=sgqlc.types.ArgDict(
            (
                (
                    "collection",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="collection",
                        default=None,
                    ),
                ),
                (
                    "scope_by_actor",
                    sgqlc.types.Arg(Boolean, graphql_name="scopeByActor", default=None),
                ),
            )
        ),
    )

    document = sgqlc.types.Field(
        NerdStorageDocument,
        graphql_name="document",
        args=sgqlc.types.ArgDict(
            (
                (
                    "collection",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="collection",
                        default=None,
                    ),
                ),
                (
                    "document_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="documentId",
                        default=None,
                    ),
                ),
                (
                    "scope_by_actor",
                    sgqlc.types.Arg(Boolean, graphql_name="scopeByActor", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `collection` (`String!`)
    * `document_id` (`String!`)
    * `scope_by_actor` (`Boolean`)
    """


class NerdStorageVaultActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("secret", "secrets")
    secret = sgqlc.types.Field(
        "NerdStorageVaultSecret",
        graphql_name="secret",
        args=sgqlc.types.ArgDict(
            (
                (
                    "key",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="key", default=None
                    ),
                ),
            )
        ),
    )

    secrets = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("NerdStorageVaultSecret"))
        ),
        graphql_name="secrets",
    )


class NerdStorageVaultDeleteSecretResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "status")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("NerdStorageVaultResultError")),
        graphql_name="errors",
    )

    status = sgqlc.types.Field(
        sgqlc.types.non_null(NerdStorageVaultResultStatus), graphql_name="status"
    )


class NerdStorageVaultResultError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(String, graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(NerdStorageVaultErrorType), graphql_name="type"
    )


class NerdStorageVaultSecret(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("key", "value")
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    value = sgqlc.types.Field(sgqlc.types.non_null(SecureValue), graphql_name="value")


class NerdStorageVaultWriteSecretResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "status")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(NerdStorageVaultResultError)),
        graphql_name="errors",
    )

    status = sgqlc.types.Field(
        sgqlc.types.non_null(NerdStorageVaultResultStatus), graphql_name="status"
    )


class NerdpackAllowListResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nerdpack", "results_per_account")
    nerdpack = sgqlc.types.Field(
        sgqlc.types.non_null("NerdpackData"), graphql_name="nerdpack"
    )

    results_per_account = sgqlc.types.Field(
        sgqlc.types.list_of("NerdpackMutationResultPerAccount"),
        graphql_name="resultsPerAccount",
    )


class NerdpackAllowedAccount(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id",)
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")


class NerdpackAssetInfo(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("name", "size_in_bytes")
    name = sgqlc.types.Field(String, graphql_name="name")

    size_in_bytes = sgqlc.types.Field(Int, graphql_name="sizeInBytes")


class NerdpackData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "allowed_accounts",
        "id",
        "subscription_model",
        "subscriptions",
        "versions",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    allowed_accounts = sgqlc.types.Field(
        sgqlc.types.list_of(NerdpackAllowedAccount), graphql_name="allowedAccounts"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    subscription_model = sgqlc.types.Field(
        NerdpackSubscriptionModel, graphql_name="subscriptionModel"
    )

    subscriptions = sgqlc.types.Field(
        sgqlc.types.list_of("NerdpackSubscription"), graphql_name="subscriptions"
    )

    versions = sgqlc.types.Field(
        "NerdpackVersionsResult",
        graphql_name="versions",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        NerdpackVersionFilter, graphql_name="filter", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `filter` (`NerdpackVersionFilter`)
    """


class NerdpackMutationResultPerAccount(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "reason", "result")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    reason = sgqlc.types.Field(NerdpackMutationErrorType, graphql_name="reason")

    result = sgqlc.types.Field(
        sgqlc.types.non_null(NerdpackMutationResult), graphql_name="result"
    )


class NerdpackNerdpacks(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("effective_subscribed_versions", "nerdpack", "subscribable")
    effective_subscribed_versions = sgqlc.types.Field(
        sgqlc.types.list_of("NerdpackVersion"),
        graphql_name="effectiveSubscribedVersions",
        args=sgqlc.types.ArgDict(
            (
                (
                    "overrides",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(NerdpackOverrideVersionRules),
                        graphql_name="overrides",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `overrides` (`[NerdpackOverrideVersionRules]`)
    """

    nerdpack = sgqlc.types.Field(
        NerdpackData,
        graphql_name="nerdpack",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    subscribable = sgqlc.types.Field(
        sgqlc.types.list_of(NerdpackData),
        graphql_name="subscribable",
        args=sgqlc.types.ArgDict(
            (
                (
                    "nerdpack_filter",
                    sgqlc.types.Arg(
                        NerdpackDataFilter, graphql_name="nerdpackFilter", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `nerdpack_filter` (`NerdpackDataFilter`)
    """


class NerdpackRemovedTagInfo(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nerdpack_id", "tag_name", "version")
    nerdpack_id = sgqlc.types.Field(ID, graphql_name="nerdpackId")

    tag_name = sgqlc.types.Field(NerdpackTagName, graphql_name="tagName")

    version = sgqlc.types.Field(SemVer, graphql_name="version")


class NerdpackRemovedTagResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("removed_tag_info", "status")
    removed_tag_info = sgqlc.types.Field(
        NerdpackRemovedTagInfo, graphql_name="removedTagInfo"
    )

    status = sgqlc.types.Field(NerdpackRemovedTagResponseType, graphql_name="status")


class NerdpackSubscribeResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nerdpack", "results_per_account", "tag")
    nerdpack = sgqlc.types.Field(
        sgqlc.types.non_null(NerdpackData), graphql_name="nerdpack"
    )

    results_per_account = sgqlc.types.Field(
        sgqlc.types.list_of(NerdpackMutationResultPerAccount),
        graphql_name="resultsPerAccount",
    )

    tag = sgqlc.types.Field(NerdpackTagName, graphql_name="tag")


class NerdpackSubscription(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("access_type", "account_id", "nerdpack_version", "tag")
    access_type = sgqlc.types.Field(
        sgqlc.types.list_of(NerdpackSubscriptionAccessType), graphql_name="accessType"
    )

    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    nerdpack_version = sgqlc.types.Field(
        "NerdpackVersion", graphql_name="nerdpackVersion"
    )

    tag = sgqlc.types.Field(NerdpackTagName, graphql_name="tag")


class NerdpackUnsubscribeResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nerdpack", "results_per_account")
    nerdpack = sgqlc.types.Field(
        sgqlc.types.non_null(NerdpackData), graphql_name="nerdpack"
    )

    results_per_account = sgqlc.types.Field(
        sgqlc.types.list_of(NerdpackMutationResultPerAccount),
        graphql_name="resultsPerAccount",
    )


class NerdpackVersion(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "assets",
        "cli_version",
        "created_at",
        "created_by_user",
        "description",
        "display_name",
        "icon",
        "nerdpack_id",
        "repository_url",
        "sdk_version",
        "subscription_model",
        "tags",
        "version",
    )
    assets = sgqlc.types.Field(
        sgqlc.types.list_of(NerdpackAssetInfo), graphql_name="assets"
    )

    cli_version = sgqlc.types.Field(SemVer, graphql_name="cliVersion")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    created_by_user = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="createdByUser"
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    icon = sgqlc.types.Field(String, graphql_name="icon")

    nerdpack_id = sgqlc.types.Field(ID, graphql_name="nerdpackId")

    repository_url = sgqlc.types.Field(String, graphql_name="repositoryUrl")

    sdk_version = sgqlc.types.Field(String, graphql_name="sdkVersion")

    subscription_model = sgqlc.types.Field(
        NerdpackSubscriptionModel, graphql_name="subscriptionModel"
    )

    tags = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(NerdpackTagName)), graphql_name="tags"
    )

    version = sgqlc.types.Field(sgqlc.types.non_null(SemVer), graphql_name="version")


class NerdpackVersionsResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "results", "total_count")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    results = sgqlc.types.Field(
        sgqlc.types.list_of(NerdpackVersion), graphql_name="results"
    )

    total_count = sgqlc.types.Field(Int, graphql_name="totalCount")


class Nr1CatalogActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "alert_policy_template",
        "categories",
        "dashboard_template",
        "data_source",
        "nerdpack",
        "nerdpacks",
        "quickstart",
        "quickstarts",
        "search",
    )
    alert_policy_template = sgqlc.types.Field(
        "Nr1CatalogAlertPolicyTemplate",
        graphql_name="alertPolicyTemplate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    categories = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("Nr1CatalogCategory")),
        graphql_name="categories",
    )

    dashboard_template = sgqlc.types.Field(
        "Nr1CatalogDashboardTemplate",
        graphql_name="dashboardTemplate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    data_source = sgqlc.types.Field(
        "Nr1CatalogDataSource",
        graphql_name="dataSource",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    nerdpack = sgqlc.types.Field(
        "Nr1CatalogNerdpack",
        graphql_name="nerdpack",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    nerdpacks = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("Nr1CatalogNerdpack")),
        graphql_name="nerdpacks",
    )

    quickstart = sgqlc.types.Field(
        "Nr1CatalogQuickstart",
        graphql_name="quickstart",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    quickstarts = sgqlc.types.Field(
        "Nr1CatalogQuickstartsListing",
        graphql_name="quickstarts",
        args=sgqlc.types.ArgDict(
            (("cursor", sgqlc.types.Arg(String, graphql_name="cursor", default=None)),)
        ),
    )

    search = sgqlc.types.Field(
        "Nr1CatalogSearchResponse",
        graphql_name="search",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        Nr1CatalogSearchFilter, graphql_name="filter", default=None
                    ),
                ),
                ("query", sgqlc.types.Arg(String, graphql_name="query", default=None)),
                (
                    "sort_by",
                    sgqlc.types.Arg(
                        Nr1CatalogSearchSortOption,
                        graphql_name="sortBy",
                        default="ALPHABETICAL",
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `filter` (`Nr1CatalogSearchFilter`)
    * `query` (`String`)
    * `sort_by` (`Nr1CatalogSearchSortOption`) (default:
      `ALPHABETICAL`)
    """


class Nr1CatalogAlertConditionOutline(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("alert_condition_template", "id")
    alert_condition_template = sgqlc.types.Field(
        sgqlc.types.non_null("Nr1CatalogAlertConditionTemplate"),
        graphql_name="alertConditionTemplate",
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class Nr1CatalogAlertConditionTemplate(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "metadata")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    metadata = sgqlc.types.Field(
        sgqlc.types.non_null("Nr1CatalogAlertConditionTemplateMetadata"),
        graphql_name="metadata",
    )


class Nr1CatalogAlertConditionTemplateMetadata(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "display_name", "type")
    description = sgqlc.types.Field(String, graphql_name="description")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogAlertConditionType), graphql_name="type"
    )


class Nr1CatalogAlertPolicyOutline(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("conditions", "id")
    conditions = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogAlertConditionOutline)),
        graphql_name="conditions",
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class Nr1CatalogAlertPolicyTemplate(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "metadata", "support_level", "updated_at")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    metadata = sgqlc.types.Field(
        "Nr1CatalogAlertPolicyTemplateMetadata", graphql_name="metadata"
    )

    support_level = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogSupportLevel), graphql_name="supportLevel"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )


class Nr1CatalogAlertPolicyTemplateMetadata(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "authors",
        "categories",
        "category_terms",
        "conditions",
        "display_name",
        "icon",
        "required_data_sources",
    )
    authors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("Nr1CatalogAuthor"))
        ),
        graphql_name="authors",
    )

    categories = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("Nr1CatalogCategory"))
        ),
        graphql_name="categories",
    )

    category_terms = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="categoryTerms",
    )

    conditions = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogAlertConditionTemplate))
        ),
        graphql_name="conditions",
    )

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    icon = sgqlc.types.Field("Nr1CatalogIcon", graphql_name="icon")

    required_data_sources = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("Nr1CatalogDataSource"))
        ),
        graphql_name="requiredDataSources",
    )


class Nr1CatalogAuthor(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("name",)
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class Nr1CatalogCategory(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("display_name", "slug", "terms")
    display_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="displayName"
    )

    slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="slug")

    terms = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="terms",
    )


class Nr1CatalogCategoryFacet(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "display_name")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")

    display_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="displayName"
    )


class Nr1CatalogCommunityContactChannel(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("url",)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class Nr1CatalogComponentFacet(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("component", "count")
    component = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogSearchComponentType), graphql_name="component"
    )

    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")


class Nr1CatalogDashboardOutline(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("dashboard_guid",)
    dashboard_guid = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGuid), graphql_name="dashboardGuid"
    )


class Nr1CatalogDashboardTemplate(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "metadata", "support_level", "updated_at")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    metadata = sgqlc.types.Field(
        sgqlc.types.non_null("Nr1CatalogDashboardTemplateMetadata"),
        graphql_name="metadata",
    )

    support_level = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogSupportLevel), graphql_name="supportLevel"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )


class Nr1CatalogDashboardTemplateMetadata(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "authors",
        "categories",
        "category_terms",
        "description",
        "display_name",
        "previews",
        "required_data_sources",
    )
    authors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogAuthor))
        ),
        graphql_name="authors",
    )

    categories = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogCategory))
        ),
        graphql_name="categories",
    )

    category_terms = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="categoryTerms",
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    previews = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogPreview))
        ),
        graphql_name="previews",
    )

    required_data_sources = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("Nr1CatalogDataSource"))
        ),
        graphql_name="requiredDataSources",
    )


class Nr1CatalogDataSource(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "metadata")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    metadata = sgqlc.types.Field(
        sgqlc.types.non_null("Nr1CatalogDataSourceMetadata"), graphql_name="metadata"
    )


class Nr1CatalogDataSourceInstall(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("fallback", "primary")
    fallback = sgqlc.types.Field(
        "Nr1CatalogDataSourceInstallDirective", graphql_name="fallback"
    )

    primary = sgqlc.types.Field(
        sgqlc.types.non_null("Nr1CatalogDataSourceInstallDirective"),
        graphql_name="primary",
    )


class Nr1CatalogDataSourceMetadata(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "auto_install_alert_policy_templates",
        "auto_install_dashboard_templates",
        "categories",
        "description",
        "display_name",
        "icon",
        "install",
        "keywords",
    )
    auto_install_alert_policy_templates = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogAlertPolicyTemplate))
        ),
        graphql_name="autoInstallAlertPolicyTemplates",
    )

    auto_install_dashboard_templates = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogDashboardTemplate))
        ),
        graphql_name="autoInstallDashboardTemplates",
    )

    categories = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogCategory))
        ),
        graphql_name="categories",
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    icon = sgqlc.types.Field("Nr1CatalogIcon", graphql_name="icon")

    install = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogDataSourceInstall), graphql_name="install"
    )

    keywords = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="keywords",
    )


class Nr1CatalogEmailContactChannel(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("address",)
    address = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="address")


class Nr1CatalogIcon(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("url",)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class Nr1CatalogInstallAlertPolicyTemplateResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("alert_policy_template", "created_alert_policy")
    alert_policy_template = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogAlertPolicyTemplate),
        graphql_name="alertPolicyTemplate",
    )

    created_alert_policy = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogAlertPolicyOutline),
        graphql_name="createdAlertPolicy",
    )


class Nr1CatalogInstallDashboardTemplateResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("created_dashboard", "dashboard_template")
    created_dashboard = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogDashboardOutline),
        graphql_name="createdDashboard",
    )

    dashboard_template = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogDashboardTemplate),
        graphql_name="dashboardTemplate",
    )


class Nr1CatalogInstallPlanStep(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "description",
        "display_name",
        "fallback",
        "heading",
        "id",
        "primary",
        "target",
    )
    description = sgqlc.types.Field(String, graphql_name="description")

    display_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="displayName"
    )

    fallback = sgqlc.types.Field(
        Nr1CatalogInstallPlanDirective, graphql_name="fallback"
    )

    heading = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="heading")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    primary = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogInstallPlanDirective), graphql_name="primary"
    )

    target = sgqlc.types.Field(
        sgqlc.types.non_null("Nr1CatalogInstallPlanTarget"), graphql_name="target"
    )


class Nr1CatalogInstallPlanTarget(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("destination", "os", "type")
    destination = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogInstallPlanDestination),
        graphql_name="destination",
    )

    os = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(Nr1CatalogInstallPlanOperatingSystem)
            )
        ),
        graphql_name="os",
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogInstallPlanTargetType), graphql_name="type"
    )


class Nr1CatalogIssuesContactChannel(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("url",)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class Nr1CatalogLinkInstallDirective(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("url",)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class Nr1CatalogNerdletInstallDirective(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nerdlet_id", "nerdlet_state", "requires_account")
    nerdlet_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="nerdletId")

    nerdlet_state = sgqlc.types.Field(
        Nr1CatalogRawNerdletState, graphql_name="nerdletState"
    )

    requires_account = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="requiresAccount"
    )


class Nr1CatalogNerdpack(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "metadata", "visibility")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    metadata = sgqlc.types.Field("Nr1CatalogNerdpackMetadata", graphql_name="metadata")

    visibility = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogNerdpackVisibility), graphql_name="visibility"
    )


class Nr1CatalogNerdpackMetadata(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "additional_info",
        "categories",
        "category_terms",
        "description",
        "details",
        "display_name",
        "documentation",
        "icon",
        "included_artifact_types",
        "keywords",
        "nerdpack_items",
        "previews",
        "publish_date",
        "repository",
        "support",
        "tagline",
        "version",
        "whats_new",
    )
    additional_info = sgqlc.types.Field(
        String,
        graphql_name="additionalInfo",
        args=sgqlc.types.ArgDict(
            (
                (
                    "format",
                    sgqlc.types.Arg(
                        Nr1CatalogRenderFormat,
                        graphql_name="format",
                        default="MARKDOWN",
                    ),
                ),
            )
        ),
    )

    categories = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogCategory))
        ),
        graphql_name="categories",
    )

    category_terms = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="categoryTerms",
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    details = sgqlc.types.Field(String, graphql_name="details")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    documentation = sgqlc.types.Field(
        String,
        graphql_name="documentation",
        args=sgqlc.types.ArgDict(
            (
                (
                    "format",
                    sgqlc.types.Arg(
                        Nr1CatalogRenderFormat,
                        graphql_name="format",
                        default="MARKDOWN",
                    ),
                ),
            )
        ),
    )

    icon = sgqlc.types.Field(Nr1CatalogIcon, graphql_name="icon")

    included_artifact_types = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="includedArtifactTypes"
    )

    keywords = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="keywords",
    )

    nerdpack_items = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogNerdpackItem))
        ),
        graphql_name="nerdpackItems",
    )

    previews = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogPreview))
        ),
        graphql_name="previews",
    )

    publish_date = sgqlc.types.Field(DateTime, graphql_name="publishDate")

    repository = sgqlc.types.Field(String, graphql_name="repository")

    support = sgqlc.types.Field(
        sgqlc.types.non_null("Nr1CatalogSupportChannels"), graphql_name="support"
    )

    tagline = sgqlc.types.Field(String, graphql_name="tagline")

    version = sgqlc.types.Field(sgqlc.types.non_null(SemVer), graphql_name="version")

    whats_new = sgqlc.types.Field("Nr1CatalogReleaseNote", graphql_name="whatsNew")


class Nr1CatalogQuickstart(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("featured", "id", "metadata", "source_url", "support_level")
    featured = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="featured")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    metadata = sgqlc.types.Field(
        "Nr1CatalogQuickstartMetadata", graphql_name="metadata"
    )

    source_url = sgqlc.types.Field(String, graphql_name="sourceUrl")

    support_level = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogSupportLevel), graphql_name="supportLevel"
    )


class Nr1CatalogQuickstartMetadata(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "authors",
        "categories",
        "category_terms",
        "data_sources",
        "description",
        "display_name",
        "icon",
        "installer",
        "keywords",
        "quickstart_components",
        "slug",
        "summary",
    )
    authors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogAuthor))
        ),
        graphql_name="authors",
    )

    categories = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogCategory))
        ),
        graphql_name="categories",
    )

    category_terms = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="categoryTerms",
    )

    data_sources = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogDataSource))
        ),
        graphql_name="dataSources",
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    icon = sgqlc.types.Field(Nr1CatalogIcon, graphql_name="icon")

    installer = sgqlc.types.Field(Nr1CatalogInstaller, graphql_name="installer")

    keywords = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="keywords",
    )

    quickstart_components = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogQuickstartComponent))
        ),
        graphql_name="quickstartComponents",
    )

    slug = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="slug")

    summary = sgqlc.types.Field(String, graphql_name="summary")


class Nr1CatalogQuickstartsListing(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "results", "total_count")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    results = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogQuickstart))
        ),
        graphql_name="results",
    )

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class Nr1CatalogReleaseNote(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("changes", "version")
    changes = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="changes")

    version = sgqlc.types.Field(sgqlc.types.non_null(SemVer), graphql_name="version")


class Nr1CatalogSearchFacets(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("categories", "components", "featured", "types")
    categories = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogCategoryFacet))
        ),
        graphql_name="categories",
    )

    components = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogComponentFacet))
        ),
        graphql_name="components",
    )

    featured = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="featured")

    types = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("Nr1CatalogSearchResultTypeFacet"))
        ),
        graphql_name="types",
    )


class Nr1CatalogSearchResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("facets", "next_cursor", "results", "total_count")
    facets = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogSearchFacets), graphql_name="facets"
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    results = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("Nr1CatalogSearchResult"))
        ),
        graphql_name="results",
    )

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class Nr1CatalogSearchResultTypeFacet(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "type")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogSearchResultType), graphql_name="type"
    )


class Nr1CatalogSubmitMetadataError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "field", "type")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    field = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="field"
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogSubmitMetadataErrorType), graphql_name="type"
    )


class Nr1CatalogSubmitMetadataResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "nerdpack", "result")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogSubmitMetadataError)),
        graphql_name="errors",
    )

    nerdpack = sgqlc.types.Field(Nr1CatalogNerdpack, graphql_name="nerdpack")

    result = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogMutationResult), graphql_name="result"
    )


class Nr1CatalogSupportChannels(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("community", "email", "issues")
    community = sgqlc.types.Field(
        Nr1CatalogCommunityContactChannel, graphql_name="community"
    )

    email = sgqlc.types.Field(Nr1CatalogEmailContactChannel, graphql_name="email")

    issues = sgqlc.types.Field(Nr1CatalogIssuesContactChannel, graphql_name="issues")


class NrdbMetadata(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("event_types", "facets", "messages", "time_window")
    event_types = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="eventTypes"
    )

    facets = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="facets")

    messages = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="messages")

    time_window = sgqlc.types.Field("NrdbMetadataTimeWindow", graphql_name="timeWindow")


class NrdbMetadataTimeWindow(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("begin", "compare_with", "end", "since", "until")
    begin = sgqlc.types.Field(EpochMilliseconds, graphql_name="begin")

    compare_with = sgqlc.types.Field(String, graphql_name="compareWith")

    end = sgqlc.types.Field(EpochMilliseconds, graphql_name="end")

    since = sgqlc.types.Field(String, graphql_name="since")

    until = sgqlc.types.Field(String, graphql_name="until")


class NrdbQueryProgress(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "completed",
        "query_id",
        "result_expiration",
        "retry_after",
        "retry_deadline",
    )
    completed = sgqlc.types.Field(Boolean, graphql_name="completed")

    query_id = sgqlc.types.Field(ID, graphql_name="queryId")

    result_expiration = sgqlc.types.Field(Seconds, graphql_name="resultExpiration")

    retry_after = sgqlc.types.Field(Seconds, graphql_name="retryAfter")

    retry_deadline = sgqlc.types.Field(Seconds, graphql_name="retryDeadline")


class NrdbResultContainer(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "current_results",
        "embedded_chart_url",
        "event_definitions",
        "metadata",
        "nrql",
        "other_result",
        "previous_results",
        "query_progress",
        "raw_response",
        "results",
        "static_chart_url",
        "suggested_facets",
        "suggested_queries",
        "total_result",
    )
    current_results = sgqlc.types.Field(
        sgqlc.types.list_of(NrdbResult), graphql_name="currentResults"
    )

    embedded_chart_url = sgqlc.types.Field(
        String,
        graphql_name="embeddedChartUrl",
        args=sgqlc.types.ArgDict(
            (
                (
                    "chart_type",
                    sgqlc.types.Arg(
                        EmbeddedChartType, graphql_name="chartType", default=None
                    ),
                ),
            )
        ),
    )

    event_definitions = sgqlc.types.Field(
        sgqlc.types.list_of(EventDefinition), graphql_name="eventDefinitions"
    )

    metadata = sgqlc.types.Field(NrdbMetadata, graphql_name="metadata")

    nrql = sgqlc.types.Field(Nrql, graphql_name="nrql")

    other_result = sgqlc.types.Field(NrdbResult, graphql_name="otherResult")

    previous_results = sgqlc.types.Field(
        sgqlc.types.list_of(NrdbResult), graphql_name="previousResults"
    )

    query_progress = sgqlc.types.Field(NrdbQueryProgress, graphql_name="queryProgress")

    raw_response = sgqlc.types.Field(NrdbRawResults, graphql_name="rawResponse")

    results = sgqlc.types.Field(sgqlc.types.list_of(NrdbResult), graphql_name="results")

    static_chart_url = sgqlc.types.Field(
        String,
        graphql_name="staticChartUrl",
        args=sgqlc.types.ArgDict(
            (
                (
                    "chart_type",
                    sgqlc.types.Arg(
                        ChartImageType, graphql_name="chartType", default=None
                    ),
                ),
                (
                    "format",
                    sgqlc.types.Arg(
                        ChartFormatType, graphql_name="format", default="PNG"
                    ),
                ),
                ("height", sgqlc.types.Arg(Int, graphql_name="height", default=None)),
                ("width", sgqlc.types.Arg(Int, graphql_name="width", default=None)),
            )
        ),
    )

    suggested_facets = sgqlc.types.Field(
        sgqlc.types.list_of("NrqlFacetSuggestion"), graphql_name="suggestedFacets"
    )

    suggested_queries = sgqlc.types.Field(
        "SuggestedNrqlQueryResponse",
        graphql_name="suggestedQueries",
        args=sgqlc.types.ArgDict(
            (
                (
                    "anomaly_time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="anomalyTimeWindow", default=None
                    ),
                ),
            )
        ),
    )

    total_result = sgqlc.types.Field(NrdbResult, graphql_name="totalResult")


class NrqlDropRulesAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("list",)
    list = sgqlc.types.Field("NrqlDropRulesListDropRulesResult", graphql_name="list")


class NrqlDropRulesCreateDropRuleFailure(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error", "submitted")
    error = sgqlc.types.Field(
        sgqlc.types.non_null("NrqlDropRulesError"), graphql_name="error"
    )

    submitted = sgqlc.types.Field(
        sgqlc.types.non_null("NrqlDropRulesCreateDropRuleSubmission"),
        graphql_name="submitted",
    )


class NrqlDropRulesCreateDropRuleResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("failures", "successes")
    failures = sgqlc.types.Field(
        sgqlc.types.list_of(NrqlDropRulesCreateDropRuleFailure), graphql_name="failures"
    )

    successes = sgqlc.types.Field(
        sgqlc.types.list_of("NrqlDropRulesDropRule"), graphql_name="successes"
    )


class NrqlDropRulesCreateDropRuleSubmission(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "action", "description", "nrql")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    action = sgqlc.types.Field(
        sgqlc.types.non_null(NrqlDropRulesAction), graphql_name="action"
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    nrql = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="nrql")


class NrqlDropRulesDeleteDropRuleFailure(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error", "submitted")
    error = sgqlc.types.Field(
        sgqlc.types.non_null("NrqlDropRulesError"), graphql_name="error"
    )

    submitted = sgqlc.types.Field(
        sgqlc.types.non_null("NrqlDropRulesDeleteDropRuleSubmission"),
        graphql_name="submitted",
    )


class NrqlDropRulesDeleteDropRuleResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("failures", "successes")
    failures = sgqlc.types.Field(
        sgqlc.types.list_of(NrqlDropRulesDeleteDropRuleFailure), graphql_name="failures"
    )

    successes = sgqlc.types.Field(
        sgqlc.types.list_of("NrqlDropRulesDropRule"), graphql_name="successes"
    )


class NrqlDropRulesDeleteDropRuleSubmission(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "rule_id")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    rule_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="ruleId")


class NrqlDropRulesDropRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account",
        "account_id",
        "action",
        "created_at",
        "created_by",
        "creator",
        "description",
        "id",
        "nrql",
        "source",
    )
    account = sgqlc.types.Field(AccountReference, graphql_name="account")

    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    action = sgqlc.types.Field(
        sgqlc.types.non_null(NrqlDropRulesAction), graphql_name="action"
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    created_by = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="createdBy")

    creator = sgqlc.types.Field("UserReference", graphql_name="creator")

    description = sgqlc.types.Field(String, graphql_name="description")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    nrql = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="nrql")

    source = sgqlc.types.Field(String, graphql_name="source")


class NrqlDropRulesError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "reason")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    reason = sgqlc.types.Field(
        sgqlc.types.non_null(NrqlDropRulesErrorReason), graphql_name="reason"
    )


class NrqlDropRulesListDropRulesResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("error", "rules")
    error = sgqlc.types.Field(NrqlDropRulesError, graphql_name="error")

    rules = sgqlc.types.Field(
        sgqlc.types.list_of(NrqlDropRulesDropRule), graphql_name="rules"
    )


class NrqlFacetSuggestion(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attributes", "nrql")
    attributes = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="attributes"
    )

    nrql = sgqlc.types.Field(Nrql, graphql_name="nrql")


class NrqlHistoricalQuery(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "nrql", "timestamp")
    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    nrql = sgqlc.types.Field(Nrql, graphql_name="nrql")

    timestamp = sgqlc.types.Field(EpochSeconds, graphql_name="timestamp")


class Organization(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_management",
        "account_shares",
        "administrator",
        "authorization_management",
        "customer_id",
        "id",
        "name",
        "telemetry_id",
        "user_management",
    )
    account_management = sgqlc.types.Field(
        AccountManagementOrganizationStitchedFields, graphql_name="accountManagement"
    )

    account_shares = sgqlc.types.Field(
        "OrganizationAccountShares",
        graphql_name="accountShares",
        args=sgqlc.types.ArgDict(
            (
                (
                    "limiting_role_id",
                    sgqlc.types.Arg(Int, graphql_name="limitingRoleId", default=None),
                ),
                (
                    "source_organization_id",
                    sgqlc.types.Arg(
                        String, graphql_name="sourceOrganizationId", default=None
                    ),
                ),
                (
                    "target_organization_id",
                    sgqlc.types.Arg(
                        String, graphql_name="targetOrganizationId", default=None
                    ),
                ),
            )
        ),
    )

    administrator = sgqlc.types.Field(
        "OrganizationOrganizationAdministrator", graphql_name="administrator"
    )

    authorization_management = sgqlc.types.Field(
        AuthorizationManagementOrganizationStitchedFields,
        graphql_name="authorizationManagement",
    )

    customer_id = sgqlc.types.Field(String, graphql_name="customerId")

    id = sgqlc.types.Field(ID, graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    telemetry_id = sgqlc.types.Field(String, graphql_name="telemetryId")

    user_management = sgqlc.types.Field(
        "UserManagementOrganizationStitchedFields", graphql_name="userManagement"
    )


class OrganizationAccountShares(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("shared_accounts",)
    shared_accounts = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("OrganizationSharedAccount")),
        graphql_name="sharedAccounts",
    )


class OrganizationAuthenticationDomain(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "authentication_type",
        "id",
        "name",
        "organization_id",
        "provisioning_type",
    )
    authentication_type = sgqlc.types.Field(
        sgqlc.types.non_null(OrganizationAuthenticationTypeEnum),
        graphql_name="authenticationType",
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    organization_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="organizationId"
    )

    provisioning_type = sgqlc.types.Field(
        sgqlc.types.non_null(OrganizationProvisioningTypeEnum),
        graphql_name="provisioningType",
    )


class OrganizationAuthenticationDomainCollection(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("items", "next_cursor")
    items = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(OrganizationAuthenticationDomain))
        ),
        graphql_name="items",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")


class OrganizationCreateSharedAccountResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("shared_account",)
    shared_account = sgqlc.types.Field(
        "OrganizationSharedAccount", graphql_name="sharedAccount"
    )


class OrganizationCustomerOrganization(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("contract_id", "customer_id", "id", "name")
    contract_id = sgqlc.types.Field(ID, graphql_name="contractId")

    customer_id = sgqlc.types.Field(String, graphql_name="customerId")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")


class OrganizationCustomerOrganizationWrapper(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("items", "next_cursor")
    items = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(OrganizationCustomerOrganization)),
        graphql_name="items",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")


class OrganizationError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(OrganizationUpdateErrorType), graphql_name="type"
    )


class OrganizationInformation(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "name")
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")


class OrganizationOrganizationAdministrator(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("organization_id", "organization_name")
    organization_id = sgqlc.types.Field(ID, graphql_name="organizationId")

    organization_name = sgqlc.types.Field(String, graphql_name="organizationName")


class OrganizationProvisioningUpdateSubscriptionResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("enqueued", "errors")
    enqueued = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enqueued")

    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null("OrganizationProvisioningUserError")
            )
        ),
        graphql_name="errors",
    )


class OrganizationProvisioningUserError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "path")
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    path = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="path"
    )


class OrganizationRevokeSharedAccountResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("shared_account",)
    shared_account = sgqlc.types.Field(
        "OrganizationSharedAccount", graphql_name="sharedAccount"
    )


class OrganizationSharedAccount(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "id",
        "limiting_role_id",
        "name",
        "source_organization_id",
        "source_organization_name",
        "target_organization_id",
        "target_organization_name",
    )
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    limiting_role_id = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="limitingRoleId"
    )

    name = sgqlc.types.Field(String, graphql_name="name")

    source_organization_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="sourceOrganizationId"
    )

    source_organization_name = sgqlc.types.Field(
        String, graphql_name="sourceOrganizationName"
    )

    target_organization_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="targetOrganizationId"
    )

    target_organization_name = sgqlc.types.Field(
        String, graphql_name="targetOrganizationName"
    )


class OrganizationUpdateResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "organization_information")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(OrganizationError))
        ),
        graphql_name="errors",
    )

    organization_information = sgqlc.types.Field(
        OrganizationInformation, graphql_name="organizationInformation"
    )


class OrganizationUpdateSharedAccountResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("shared_account",)
    shared_account = sgqlc.types.Field(
        OrganizationSharedAccount, graphql_name="sharedAccount"
    )


class PixieAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("linked_pixie_project", "pixie_access_token")
    linked_pixie_project = sgqlc.types.Field(
        "PixiePixieProject", graphql_name="linkedPixieProject"
    )

    pixie_access_token = sgqlc.types.Field(SecureValue, graphql_name="pixieAccessToken")


class PixieActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("linked_pixie_projects",)
    linked_pixie_projects = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of("PixieLinkedPixieProject")),
        graphql_name="linkedPixieProjects",
    )


class PixieLinkPixieProjectError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(String, graphql_name="message")

    type = sgqlc.types.Field(PixieLinkPixieProjectErrorType, graphql_name="type")


class PixieLinkPixieProjectResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "linked_pixie_project", "success")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(PixieLinkPixieProjectError), graphql_name="errors"
    )

    linked_pixie_project = sgqlc.types.Field(
        "PixiePixieProject", graphql_name="linkedPixieProject"
    )

    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="success")


class PixieLinkedPixieProject(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "pixie_project")
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="accountId")

    pixie_project = sgqlc.types.Field(
        sgqlc.types.non_null("PixiePixieProject"), graphql_name="pixieProject"
    )


class PixiePixieProject(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("api_key", "deploy_key")
    api_key = sgqlc.types.Field(SecureValue, graphql_name="apiKey")

    deploy_key = sgqlc.types.Field(SecureValue, graphql_name="deployKey")


class PixieRecordPixieTosAcceptanceError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(String, graphql_name="message")

    type = sgqlc.types.Field(
        PixieRecordPixieTosAcceptanceErrorType, graphql_name="type"
    )


class PixieRecordPixieTosAcceptanceResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "success")
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(PixieRecordPixieTosAcceptanceError), graphql_name="errors"
    )

    success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="success")


class QueryHistoryActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nrql",)
    nrql = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("QueryHistoryNrqlHistoryResult")),
        graphql_name="nrql",
        args=sgqlc.types.ArgDict(
            (
                (
                    "options",
                    sgqlc.types.Arg(
                        QueryHistoryQueryHistoryOptionsInput,
                        graphql_name="options",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `options` (`QueryHistoryQueryHistoryOptionsInput`)
    """


class QueryHistoryNrqlHistoryResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_ids", "created_at", "query")
    account_ids = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name="accountIds"
    )

    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")

    query = sgqlc.types.Field(Nrql, graphql_name="query")


class ReferenceEntityCreateRepositoryError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("guid", "message", "type")
    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="message")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(ReferenceEntityCreateRepositoryErrorType),
        graphql_name="type",
    )


class ReferenceEntityCreateRepositoryResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("created", "failures", "updated")
    created = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EntityGuid))),
        graphql_name="created",
    )

    failures = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(ReferenceEntityCreateRepositoryError)
            )
        ),
        graphql_name="failures",
    )

    updated = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(EntityGuid))),
        graphql_name="updated",
    )


class RequestContext(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("api_key", "user_id")
    api_key = sgqlc.types.Field(String, graphql_name="apiKey")

    user_id = sgqlc.types.Field(ID, graphql_name="userId")


class RootMutationType(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_management_create_account",
        "account_management_update_account",
        "agent_application_create_browser",
        "agent_application_create_mobile",
        "agent_application_delete",
        "agent_application_enable_apm_browser",
        "agent_application_settings_update",
        "ai_decisions_accept_suggestion",
        "ai_decisions_create_implicit_rule",
        "ai_decisions_create_rule",
        "ai_decisions_create_suggestion",
        "ai_decisions_decline_suggestion",
        "ai_decisions_delete_merge_feedback",
        "ai_decisions_delete_rule",
        "ai_decisions_delete_suggestion",
        "ai_decisions_disable_rule",
        "ai_decisions_enable_rule",
        "ai_decisions_find_applicable_incidents",
        "ai_decisions_postpone_suggestion",
        "ai_decisions_record_merge_feedback",
        "ai_decisions_simulate",
        "ai_decisions_update_implicit_rule",
        "ai_decisions_update_rule",
        "ai_issues_ack_issue",
        "ai_issues_close_incident",
        "ai_issues_resolve_issue",
        "ai_issues_unack_issue",
        "ai_issues_update_grace_period",
        "ai_issues_update_issue_ttl",
        "ai_notifications_create_channel",
        "ai_notifications_create_destination",
        "ai_notifications_delete_channel",
        "ai_notifications_delete_destination",
        "ai_notifications_test_channel",
        "ai_notifications_test_channel_by_id",
        "ai_notifications_test_destination",
        "ai_notifications_test_destination_by_id",
        "ai_notifications_update_channel",
        "ai_notifications_update_destination",
        "ai_topology_collector_create_edges",
        "ai_topology_collector_create_vertices",
        "ai_topology_collector_delete_edges",
        "ai_topology_collector_delete_vertices",
        "ai_workflows_create_workflow",
        "ai_workflows_delete_workflow",
        "ai_workflows_test_workflow",
        "ai_workflows_update_workflow",
        "alerts_condition_delete",
        "alerts_muting_rule_create",
        "alerts_muting_rule_delete",
        "alerts_muting_rule_update",
        "alerts_notification_channel_create",
        "alerts_notification_channel_delete",
        "alerts_notification_channel_update",
        "alerts_notification_channels_add_to_policy",
        "alerts_notification_channels_remove_from_policy",
        "alerts_nrql_condition_baseline_create",
        "alerts_nrql_condition_baseline_update",
        "alerts_nrql_condition_static_create",
        "alerts_nrql_condition_static_update",
        "alerts_policy_create",
        "alerts_policy_delete",
        "alerts_policy_update",
        "api_access_create_keys",
        "api_access_delete_keys",
        "api_access_update_keys",
        "authorization_management_grant_access",
        "authorization_management_revoke_access",
        "change_tracking_create_deployment",
        "cloud_configure_integration",
        "cloud_disable_integration",
        "cloud_link_account",
        "cloud_migrate_aws_gov_cloud_to_assume_role",
        "cloud_rename_account",
        "cloud_unlink_account",
        "dashboard_add_widgets_to_page",
        "dashboard_create",
        "dashboard_create_snapshot_url",
        "dashboard_delete",
        "dashboard_undelete",
        "dashboard_update",
        "dashboard_update_page",
        "dashboard_update_widgets_in_page",
        "dashboard_widget_revoke_live_url",
        "data_management_copy_retentions",
        "data_management_create_event_retention_rule",
        "data_management_create_retention_rules",
        "data_management_delete_event_retention_rule",
        "data_management_update_feature_settings",
        "edge_create_trace_filter_rules",
        "edge_create_trace_observer",
        "edge_delete_trace_filter_rules",
        "edge_delete_trace_observers",
        "edge_update_trace_observers",
        "entity_delete",
        "entity_golden_metrics_override",
        "entity_golden_metrics_reset",
        "entity_golden_tags_override",
        "entity_golden_tags_reset",
        "entity_relationship_user_defined_create_or_replace",
        "entity_relationship_user_defined_delete",
        "errors_inbox_assign_error_group",
        "errors_inbox_delete_error_group_resource",
        "errors_inbox_update_error_group_state",
        "events_to_metrics_create_rule",
        "events_to_metrics_delete_rule",
        "events_to_metrics_update_rule",
        "historical_data_export_cancel_export",
        "historical_data_export_create_export",
        "incident_intelligence_environment_consent_accounts",
        "incident_intelligence_environment_consent_authorized_accounts",
        "incident_intelligence_environment_delete_environment",
        "incident_intelligence_environment_dissent_accounts",
        "installation_create_install_status",
        "installation_create_recipe_event",
        "installation_delete_install",
        "key_transaction_create",
        "key_transaction_delete",
        "key_transaction_update",
        "log_configurations_create_data_partition_rule",
        "log_configurations_create_obfuscation_expression",
        "log_configurations_create_obfuscation_rule",
        "log_configurations_create_parsing_rule",
        "log_configurations_delete_data_partition_rule",
        "log_configurations_delete_obfuscation_expression",
        "log_configurations_delete_obfuscation_rule",
        "log_configurations_delete_parsing_rule",
        "log_configurations_update_data_partition_rule",
        "log_configurations_update_obfuscation_expression",
        "log_configurations_update_obfuscation_rule",
        "log_configurations_update_parsing_rule",
        "log_configurations_upsert_pipeline_configuration",
        "metric_normalization_create_rule",
        "metric_normalization_disable_rule",
        "metric_normalization_edit_rule",
        "metric_normalization_enable_rule",
        "mobile_push_notification_remove_device",
        "mobile_push_notification_send_test_push",
        "mobile_push_notification_send_test_push_to_all",
        "nerd_storage_delete_collection",
        "nerd_storage_delete_document",
        "nerd_storage_vault_delete_secret",
        "nerd_storage_vault_write_secret",
        "nerd_storage_write_document",
        "nerdpack_add_allowed_accounts",
        "nerdpack_create",
        "nerdpack_remove_allowed_accounts",
        "nerdpack_remove_version_tag",
        "nerdpack_subscribe_accounts",
        "nerdpack_tag_version",
        "nerdpack_unsubscribe_accounts",
        "nr1_catalog_install_alert_policy_template",
        "nr1_catalog_install_dashboard_template",
        "nr1_catalog_submit_metadata",
        "nrql_drop_rules_create",
        "nrql_drop_rules_delete",
        "organization_create_shared_account",
        "organization_provisioning_update_partner_subscription",
        "organization_revoke_shared_account",
        "organization_update",
        "organization_update_shared_account",
        "pixie_link_pixie_project",
        "pixie_record_pixie_tos_acceptance",
        "pixie_unlink_pixie_project",
        "reference_entity_create_or_update_repository",
        "service_level_create",
        "service_level_delete",
        "service_level_update",
        "streaming_export_create_rule",
        "streaming_export_delete_rule",
        "streaming_export_disable_rule",
        "streaming_export_enable_rule",
        "streaming_export_update_rule",
        "synthetics_create_broken_links_monitor",
        "synthetics_create_cert_check_monitor",
        "synthetics_create_private_location",
        "synthetics_create_script_api_monitor",
        "synthetics_create_script_browser_monitor",
        "synthetics_create_secure_credential",
        "synthetics_create_simple_browser_monitor",
        "synthetics_create_simple_monitor",
        "synthetics_create_step_monitor",
        "synthetics_delete_monitor",
        "synthetics_delete_private_location",
        "synthetics_delete_secure_credential",
        "synthetics_purge_private_location_queue",
        "synthetics_update_broken_links_monitor",
        "synthetics_update_cert_check_monitor",
        "synthetics_update_private_location",
        "synthetics_update_script_api_monitor",
        "synthetics_update_script_browser_monitor",
        "synthetics_update_secure_credential",
        "synthetics_update_simple_browser_monitor",
        "synthetics_update_simple_monitor",
        "synthetics_update_step_monitor",
        "tagging_add_tags_to_entity",
        "tagging_delete_tag_from_entity",
        "tagging_delete_tag_values_from_entity",
        "tagging_replace_tags_on_entity",
        "user_management_add_users_to_groups",
        "user_management_create_group",
        "user_management_create_user",
        "user_management_delete_group",
        "user_management_delete_user",
        "user_management_remove_users_from_groups",
        "user_management_update_group",
        "user_management_update_user",
        "whats_new_set_last_read_date",
        "workload_create",
        "workload_delete",
        "workload_duplicate",
        "workload_update",
    )
    account_management_create_account = sgqlc.types.Field(
        AccountManagementCreateResponse,
        graphql_name="accountManagementCreateAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "managed_account",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AccountManagementCreateInput),
                        graphql_name="managedAccount",
                        default=None,
                    ),
                ),
            )
        ),
    )

    account_management_update_account = sgqlc.types.Field(
        AccountManagementUpdateResponse,
        graphql_name="accountManagementUpdateAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "managed_account",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AccountManagementUpdateInput),
                        graphql_name="managedAccount",
                        default=None,
                    ),
                ),
            )
        ),
    )

    agent_application_create_browser = sgqlc.types.Field(
        AgentApplicationCreateBrowserResult,
        graphql_name="agentApplicationCreateBrowser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="name", default=None
                    ),
                ),
                (
                    "settings",
                    sgqlc.types.Arg(
                        AgentApplicationBrowserSettingsInput,
                        graphql_name="settings",
                        default=None,
                    ),
                ),
            )
        ),
    )

    agent_application_create_mobile = sgqlc.types.Field(
        AgentApplicationCreateMobileResult,
        graphql_name="agentApplicationCreateMobile",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="name", default=None
                    ),
                ),
            )
        ),
    )

    agent_application_delete = sgqlc.types.Field(
        AgentApplicationDeleteResult,
        graphql_name="agentApplicationDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    agent_application_enable_apm_browser = sgqlc.types.Field(
        AgentApplicationEnableBrowserResult,
        graphql_name="agentApplicationEnableApmBrowser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "settings",
                    sgqlc.types.Arg(
                        AgentApplicationBrowserSettingsInput,
                        graphql_name="settings",
                        default=None,
                    ),
                ),
            )
        ),
    )

    agent_application_settings_update = sgqlc.types.Field(
        AgentApplicationSettingsUpdateResult,
        graphql_name="agentApplicationSettingsUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "settings",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AgentApplicationSettingsUpdateInput),
                        graphql_name="settings",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_decisions_accept_suggestion = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRule),
        graphql_name="aiDecisionsAcceptSuggestion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "suggestion_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="suggestionId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_decisions_create_implicit_rule = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRule),
        graphql_name="aiDecisionsCreateImplicitRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiDecisionsRuleBlueprint),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_decisions_create_rule = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRule),
        graphql_name="aiDecisionsCreateRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiDecisionsRuleBlueprint),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_decisions_create_suggestion = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsSuggestion),
        graphql_name="aiDecisionsCreateSuggestion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "suggestion",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiDecisionsSuggestionBlueprint),
                        graphql_name="suggestion",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_decisions_decline_suggestion = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsOperationResult),
        graphql_name="aiDecisionsDeclineSuggestion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "suggestion_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="suggestionId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_decisions_delete_merge_feedback = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsOperationResult),
        graphql_name="aiDecisionsDeleteMergeFeedback",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "child_issue_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="childIssueId",
                        default=None,
                    ),
                ),
                (
                    "parent_issue_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="parentIssueId",
                        default=None,
                    ),
                ),
                (
                    "rule_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="ruleId", default=None
                    ),
                ),
            )
        ),
    )

    ai_decisions_delete_rule = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsOperationResult),
        graphql_name="aiDecisionsDeleteRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="ruleId", default=None
                    ),
                ),
            )
        ),
    )

    ai_decisions_delete_suggestion = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsOperationResult),
        graphql_name="aiDecisionsDeleteSuggestion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "suggestion_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="suggestionId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_decisions_disable_rule = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsOperationResult),
        graphql_name="aiDecisionsDisableRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="ruleId", default=None
                    ),
                ),
            )
        ),
    )

    ai_decisions_enable_rule = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsOperationResult),
        graphql_name="aiDecisionsEnableRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="ruleId", default=None
                    ),
                ),
            )
        ),
    )

    ai_decisions_find_applicable_incidents = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsApplicableIncidentSearch),
        graphql_name="aiDecisionsFindApplicableIncidents",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "search",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiDecisionsSearchBlueprint),
                        graphql_name="search",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_decisions_postpone_suggestion = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRule),
        graphql_name="aiDecisionsPostponeSuggestion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "suggestion_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="suggestionId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_decisions_record_merge_feedback = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsMergeFeedback),
        graphql_name="aiDecisionsRecordMergeFeedback",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "child_issue_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="childIssueId",
                        default=None,
                    ),
                ),
                (
                    "opinion",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiDecisionsOpinion),
                        graphql_name="opinion",
                        default=None,
                    ),
                ),
                (
                    "parent_issue_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="parentIssueId",
                        default=None,
                    ),
                ),
                (
                    "rule_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="ruleId", default=None
                    ),
                ),
            )
        ),
    )

    ai_decisions_simulate = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsSimulation),
        graphql_name="aiDecisionsSimulate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "simulation",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiDecisionsSimulationBlueprint),
                        graphql_name="simulation",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_decisions_update_implicit_rule = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRule),
        graphql_name="aiDecisionsUpdateImplicitRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiDecisionsRuleBlueprint),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
                (
                    "rule_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="ruleId", default=None
                    ),
                ),
            )
        ),
    )

    ai_decisions_update_rule = sgqlc.types.Field(
        sgqlc.types.non_null(AiDecisionsRule),
        graphql_name="aiDecisionsUpdateRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiDecisionsRuleBlueprint),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
                (
                    "rule_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="ruleId", default=None
                    ),
                ),
            )
        ),
    )

    ai_issues_ack_issue = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesIssueUserActionResponse),
        graphql_name="aiIssuesAckIssue",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "issue_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="issueId", default=None
                    ),
                ),
            )
        ),
    )

    ai_issues_close_incident = sgqlc.types.Field(
        AiIssuesIncidentUserActionResponse,
        graphql_name="aiIssuesCloseIncident",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "incident_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="incidentId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_issues_resolve_issue = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesIssueUserActionResponse),
        graphql_name="aiIssuesResolveIssue",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "issue_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="issueId", default=None
                    ),
                ),
            )
        ),
    )

    ai_issues_unack_issue = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesIssueUserActionResponse),
        graphql_name="aiIssuesUnackIssue",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "issue_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="issueId", default=None
                    ),
                ),
            )
        ),
    )

    ai_issues_update_grace_period = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesConfigurationOverrideResponse),
        graphql_name="aiIssuesUpdateGracePeriod",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "grace_period",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiIssuesGracePeriodConfigurationInput),
                        graphql_name="gracePeriod",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_issues_update_issue_ttl = sgqlc.types.Field(
        sgqlc.types.non_null(AiIssuesConfigurationOverrideResponse),
        graphql_name="aiIssuesUpdateIssueTtl",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "issue_ttl",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Seconds),
                        graphql_name="issueTtl",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_notifications_create_channel = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsChannelResponse),
        graphql_name="aiNotificationsCreateChannel",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "channel",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiNotificationsChannelInput),
                        graphql_name="channel",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_notifications_create_destination = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsDestinationResponse),
        graphql_name="aiNotificationsCreateDestination",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "destination",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiNotificationsDestinationInput),
                        graphql_name="destination",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_notifications_delete_channel = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsDeleteResponse),
        graphql_name="aiNotificationsDeleteChannel",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "channel_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="channelId", default=None
                    ),
                ),
            )
        ),
    )

    ai_notifications_delete_destination = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsDeleteResponse),
        graphql_name="aiNotificationsDeleteDestination",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "destination_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="destinationId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_notifications_test_channel = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsChannelTestResponse),
        graphql_name="aiNotificationsTestChannel",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "channel",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiNotificationsChannelInput),
                        graphql_name="channel",
                        default=None,
                    ),
                ),
                (
                    "variables",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(
                            sgqlc.types.non_null(AiNotificationsDynamicVariable)
                        ),
                        graphql_name="variables",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `channel` (`AiNotificationsChannelInput!`)
    * `variables` (`[AiNotificationsDynamicVariable!]`)
    """

    ai_notifications_test_channel_by_id = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsChannelTestResponse),
        graphql_name="aiNotificationsTestChannelById",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "channel_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="channelId", default=None
                    ),
                ),
                (
                    "variables",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(
                            sgqlc.types.non_null(AiNotificationsDynamicVariable)
                        ),
                        graphql_name="variables",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `channel_id` (`ID!`)
    * `variables` (`[AiNotificationsDynamicVariable!]`)
    """

    ai_notifications_test_destination = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsDestinationTestResponse),
        graphql_name="aiNotificationsTestDestination",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "destination",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiNotificationsDestinationInput),
                        graphql_name="destination",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_notifications_test_destination_by_id = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsDestinationTestResponse),
        graphql_name="aiNotificationsTestDestinationById",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "destination_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="destinationId",
                        default=None,
                    ),
                ),
                (
                    "update",
                    sgqlc.types.Arg(
                        AiNotificationsDestinationUpdate,
                        graphql_name="update",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_notifications_update_channel = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsChannelResponse),
        graphql_name="aiNotificationsUpdateChannel",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "channel",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiNotificationsChannelUpdate),
                        graphql_name="channel",
                        default=None,
                    ),
                ),
                (
                    "channel_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="channelId", default=None
                    ),
                ),
            )
        ),
    )

    ai_notifications_update_destination = sgqlc.types.Field(
        sgqlc.types.non_null(AiNotificationsDestinationResponse),
        graphql_name="aiNotificationsUpdateDestination",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "destination",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiNotificationsDestinationUpdate),
                        graphql_name="destination",
                        default=None,
                    ),
                ),
                (
                    "destination_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="destinationId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_topology_collector_create_edges = sgqlc.types.Field(
        sgqlc.types.non_null(AiTopologyCollectorOperationResult),
        graphql_name="aiTopologyCollectorCreateEdges",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "edges",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(AiTopologyCollectorEdgeBlueprint)
                            )
                        ),
                        graphql_name="edges",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `edges` (`[AiTopologyCollectorEdgeBlueprint!]!`)
    """

    ai_topology_collector_create_vertices = sgqlc.types.Field(
        sgqlc.types.non_null(AiTopologyCollectorOperationResult),
        graphql_name="aiTopologyCollectorCreateVertices",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "vertices",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(AiTopologyCollectorVertexBlueprint)
                            )
                        ),
                        graphql_name="vertices",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `vertices` (`[AiTopologyCollectorVertexBlueprint!]!`)
    """

    ai_topology_collector_delete_edges = sgqlc.types.Field(
        sgqlc.types.non_null(AiTopologyCollectorOperationResult),
        graphql_name="aiTopologyCollectorDeleteEdges",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "edge_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(ID))
                        ),
                        graphql_name="edgeIds",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `edge_ids` (`[ID!]!`)
    """

    ai_topology_collector_delete_vertices = sgqlc.types.Field(
        sgqlc.types.non_null(AiTopologyCollectorOperationResult),
        graphql_name="aiTopologyCollectorDeleteVertices",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "vertex_names",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(ID))
                        ),
                        graphql_name="vertexNames",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `vertex_names` (`[ID!]!`)
    """

    ai_workflows_create_workflow = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsCreateWorkflowResponse),
        graphql_name="aiWorkflowsCreateWorkflow",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "create_workflow_data",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiWorkflowsCreateWorkflowInput),
                        graphql_name="createWorkflowData",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_workflows_delete_workflow = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsDeleteWorkflowResponse),
        graphql_name="aiWorkflowsDeleteWorkflow",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "delete_channels",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="deleteChannels",
                        default=True,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    ai_workflows_test_workflow = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsTestWorkflowResponse),
        graphql_name="aiWorkflowsTestWorkflow",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "test_workflow_data",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiWorkflowsTestWorkflowInput),
                        graphql_name="testWorkflowData",
                        default=None,
                    ),
                ),
            )
        ),
    )

    ai_workflows_update_workflow = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsUpdateWorkflowResponse),
        graphql_name="aiWorkflowsUpdateWorkflow",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "delete_unused_channels",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="deleteUnusedChannels",
                        default=True,
                    ),
                ),
                (
                    "update_workflow_data",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AiWorkflowsUpdateWorkflowInput),
                        graphql_name="updateWorkflowData",
                        default=None,
                    ),
                ),
            )
        ),
    )

    alerts_condition_delete = sgqlc.types.Field(
        AlertsConditionDeleteResponse,
        graphql_name="alertsConditionDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    alerts_muting_rule_create = sgqlc.types.Field(
        AlertsMutingRule,
        graphql_name="alertsMutingRuleCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AlertsMutingRuleInput),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    alerts_muting_rule_delete = sgqlc.types.Field(
        AlertsMutingRuleDeleteResponse,
        graphql_name="alertsMutingRuleDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    alerts_muting_rule_update = sgqlc.types.Field(
        AlertsMutingRule,
        graphql_name="alertsMutingRuleUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AlertsMutingRuleUpdateInput),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    alerts_notification_channel_create = sgqlc.types.Field(
        AlertsNotificationChannelCreateResponse,
        graphql_name="alertsNotificationChannelCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "notification_channel",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            AlertsNotificationChannelCreateConfiguration
                        ),
                        graphql_name="notificationChannel",
                        default=None,
                    ),
                ),
            )
        ),
    )

    alerts_notification_channel_delete = sgqlc.types.Field(
        AlertsNotificationChannelDeleteResponse,
        graphql_name="alertsNotificationChannelDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    alerts_notification_channel_update = sgqlc.types.Field(
        AlertsNotificationChannelUpdateResponse,
        graphql_name="alertsNotificationChannelUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
                (
                    "notification_channel",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            AlertsNotificationChannelUpdateConfiguration
                        ),
                        graphql_name="notificationChannel",
                        default=None,
                    ),
                ),
            )
        ),
    )

    alerts_notification_channels_add_to_policy = sgqlc.types.Field(
        AlertsNotificationChannelsAddToPolicyResponse,
        graphql_name="alertsNotificationChannelsAddToPolicy",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "notification_channel_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(ID))
                        ),
                        graphql_name="notificationChannelIds",
                        default=None,
                    ),
                ),
                (
                    "policy_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="policyId", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `notification_channel_ids` (`[ID!]!`)
    * `policy_id` (`ID!`)
    """

    alerts_notification_channels_remove_from_policy = sgqlc.types.Field(
        AlertsNotificationChannelsRemoveFromPolicyResponse,
        graphql_name="alertsNotificationChannelsRemoveFromPolicy",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "notification_channel_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(ID))
                        ),
                        graphql_name="notificationChannelIds",
                        default=None,
                    ),
                ),
                (
                    "policy_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="policyId", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `notification_channel_ids` (`[ID!]!`)
    * `policy_id` (`ID!`)
    """

    alerts_nrql_condition_baseline_create = sgqlc.types.Field(
        "AlertsNrqlBaselineCondition",
        graphql_name="alertsNrqlConditionBaselineCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "condition",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AlertsNrqlConditionBaselineInput),
                        graphql_name="condition",
                        default=None,
                    ),
                ),
                (
                    "policy_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="policyId", default=None
                    ),
                ),
            )
        ),
    )

    alerts_nrql_condition_baseline_update = sgqlc.types.Field(
        "AlertsNrqlBaselineCondition",
        graphql_name="alertsNrqlConditionBaselineUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "condition",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AlertsNrqlConditionUpdateBaselineInput),
                        graphql_name="condition",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    alerts_nrql_condition_static_create = sgqlc.types.Field(
        "AlertsNrqlStaticCondition",
        graphql_name="alertsNrqlConditionStaticCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "condition",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AlertsNrqlConditionStaticInput),
                        graphql_name="condition",
                        default=None,
                    ),
                ),
                (
                    "policy_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="policyId", default=None
                    ),
                ),
            )
        ),
    )

    alerts_nrql_condition_static_update = sgqlc.types.Field(
        "AlertsNrqlStaticCondition",
        graphql_name="alertsNrqlConditionStaticUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "condition",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AlertsNrqlConditionUpdateStaticInput),
                        graphql_name="condition",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    alerts_policy_create = sgqlc.types.Field(
        AlertsPolicy,
        graphql_name="alertsPolicyCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "policy",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AlertsPolicyInput),
                        graphql_name="policy",
                        default=None,
                    ),
                ),
            )
        ),
    )

    alerts_policy_delete = sgqlc.types.Field(
        AlertsPolicyDeleteResponse,
        graphql_name="alertsPolicyDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    alerts_policy_update = sgqlc.types.Field(
        AlertsPolicy,
        graphql_name="alertsPolicyUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
                (
                    "policy",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AlertsPolicyUpdateInput),
                        graphql_name="policy",
                        default=None,
                    ),
                ),
            )
        ),
    )

    api_access_create_keys = sgqlc.types.Field(
        ApiAccessCreateKeyResponse,
        graphql_name="apiAccessCreateKeys",
        args=sgqlc.types.ArgDict(
            (
                (
                    "keys",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ApiAccessCreateInput),
                        graphql_name="keys",
                        default=None,
                    ),
                ),
            )
        ),
    )

    api_access_delete_keys = sgqlc.types.Field(
        ApiAccessDeleteKeyResponse,
        graphql_name="apiAccessDeleteKeys",
        args=sgqlc.types.ArgDict(
            (
                (
                    "keys",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ApiAccessDeleteInput),
                        graphql_name="keys",
                        default=None,
                    ),
                ),
            )
        ),
    )

    api_access_update_keys = sgqlc.types.Field(
        ApiAccessUpdateKeyResponse,
        graphql_name="apiAccessUpdateKeys",
        args=sgqlc.types.ArgDict(
            (
                (
                    "keys",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ApiAccessUpdateInput),
                        graphql_name="keys",
                        default=None,
                    ),
                ),
            )
        ),
    )

    authorization_management_grant_access = sgqlc.types.Field(
        AuthorizationManagementGrantAccessPayload,
        graphql_name="authorizationManagementGrantAccess",
        args=sgqlc.types.ArgDict(
            (
                (
                    "grant_access_options",
                    sgqlc.types.Arg(
                        AuthorizationManagementGrantAccess,
                        graphql_name="grantAccessOptions",
                        default=None,
                    ),
                ),
            )
        ),
    )

    authorization_management_revoke_access = sgqlc.types.Field(
        AuthorizationManagementRevokeAccessPayload,
        graphql_name="authorizationManagementRevokeAccess",
        args=sgqlc.types.ArgDict(
            (
                (
                    "revoke_access_options",
                    sgqlc.types.Arg(
                        AuthorizationManagementRevokeAccess,
                        graphql_name="revokeAccessOptions",
                        default=None,
                    ),
                ),
            )
        ),
    )

    change_tracking_create_deployment = sgqlc.types.Field(
        ChangeTrackingDeployment,
        graphql_name="changeTrackingCreateDeployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "data_handling_rules",
                    sgqlc.types.Arg(
                        ChangeTrackingDataHandlingRules,
                        graphql_name="dataHandlingRules",
                        default=None,
                    ),
                ),
                (
                    "deployment",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ChangeTrackingDeploymentInput),
                        graphql_name="deployment",
                        default=None,
                    ),
                ),
            )
        ),
    )

    cloud_configure_integration = sgqlc.types.Field(
        CloudConfigureIntegrationPayload,
        graphql_name="cloudConfigureIntegration",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "integrations",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(CloudIntegrationsInput),
                        graphql_name="integrations",
                        default=None,
                    ),
                ),
            )
        ),
    )

    cloud_disable_integration = sgqlc.types.Field(
        CloudDisableIntegrationPayload,
        graphql_name="cloudDisableIntegration",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "integrations",
                    sgqlc.types.Arg(
                        CloudDisableIntegrationsInput,
                        graphql_name="integrations",
                        default=None,
                    ),
                ),
            )
        ),
    )

    cloud_link_account = sgqlc.types.Field(
        CloudLinkAccountPayload,
        graphql_name="cloudLinkAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "accounts",
                    sgqlc.types.Arg(
                        CloudLinkCloudAccountsInput,
                        graphql_name="accounts",
                        default=None,
                    ),
                ),
            )
        ),
    )

    cloud_migrate_aws_gov_cloud_to_assume_role = sgqlc.types.Field(
        CloudMigrateAwsGovCloudToAssumeRolePayload,
        graphql_name="cloudMigrateAwsGovCloudToAssumeRole",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "accounts",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(
                                    CloudAwsGovCloudMigrateToAssumeroleInput
                                )
                            )
                        ),
                        graphql_name="accounts",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `accounts` (`[CloudAwsGovCloudMigrateToAssumeroleInput!]!`)
    """

    cloud_rename_account = sgqlc.types.Field(
        CloudRenameAccountPayload,
        graphql_name="cloudRenameAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "accounts",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(CloudRenameAccountsInput),
                        graphql_name="accounts",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `accounts` (`[CloudRenameAccountsInput]`)
    """

    cloud_unlink_account = sgqlc.types.Field(
        CloudUnlinkAccountPayload,
        graphql_name="cloudUnlinkAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "accounts",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(CloudUnlinkAccountsInput),
                        graphql_name="accounts",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `accounts` (`[CloudUnlinkAccountsInput]`)
    """

    dashboard_add_widgets_to_page = sgqlc.types.Field(
        DashboardAddWidgetsToPageResult,
        graphql_name="dashboardAddWidgetsToPage",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "widgets",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(DashboardWidgetInput)
                            )
                        ),
                        graphql_name="widgets",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `guid` (`EntityGuid!`)
    * `widgets` (`[DashboardWidgetInput!]!`)
    """

    dashboard_create = sgqlc.types.Field(
        DashboardCreateResult,
        graphql_name="dashboardCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "dashboard",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(DashboardInput),
                        graphql_name="dashboard",
                        default=None,
                    ),
                ),
            )
        ),
    )

    dashboard_create_snapshot_url = sgqlc.types.Field(
        String,
        graphql_name="dashboardCreateSnapshotUrl",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "params",
                    sgqlc.types.Arg(
                        DashboardSnapshotUrlInput, graphql_name="params", default=None
                    ),
                ),
            )
        ),
    )

    dashboard_delete = sgqlc.types.Field(
        DashboardDeleteResult,
        graphql_name="dashboardDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    dashboard_undelete = sgqlc.types.Field(
        DashboardUndeleteResult,
        graphql_name="dashboardUndelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    dashboard_update = sgqlc.types.Field(
        DashboardUpdateResult,
        graphql_name="dashboardUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dashboard",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(DashboardInput),
                        graphql_name="dashboard",
                        default=None,
                    ),
                ),
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    dashboard_update_page = sgqlc.types.Field(
        DashboardUpdatePageResult,
        graphql_name="dashboardUpdatePage",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "page",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(DashboardUpdatePageInput),
                        graphql_name="page",
                        default=None,
                    ),
                ),
            )
        ),
    )

    dashboard_update_widgets_in_page = sgqlc.types.Field(
        DashboardUpdateWidgetsInPageResult,
        graphql_name="dashboardUpdateWidgetsInPage",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "widgets",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(DashboardUpdateWidgetInput)
                            )
                        ),
                        graphql_name="widgets",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `guid` (`EntityGuid!`)
    * `widgets` (`[DashboardUpdateWidgetInput!]!`)
    """

    dashboard_widget_revoke_live_url = sgqlc.types.Field(
        DashboardRevokeLiveUrlResult,
        graphql_name="dashboardWidgetRevokeLiveUrl",
        args=sgqlc.types.ArgDict(
            (
                (
                    "uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="uuid", default=None
                    ),
                ),
            )
        ),
    )

    data_management_copy_retentions = sgqlc.types.Field(
        DataManagementBulkCopyResult,
        graphql_name="dataManagementCopyRetentions",
        args=sgqlc.types.ArgDict(
            (
                (
                    "destination_account_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(Int)),
                        graphql_name="destinationAccountIds",
                        default=None,
                    ),
                ),
                (
                    "source_account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="sourceAccountId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `destination_account_ids` (`[Int]!`)
    * `source_account_id` (`Int!`)
    """

    data_management_create_event_retention_rule = sgqlc.types.Field(
        DataManagementRule,
        graphql_name="dataManagementCreateEventRetentionRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "namespace",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="namespace",
                        default=None,
                    ),
                ),
                (
                    "retention_in_days",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="retentionInDays",
                        default=None,
                    ),
                ),
            )
        ),
    )

    data_management_create_retention_rules = sgqlc.types.Field(
        sgqlc.types.list_of(DataManagementRule),
        graphql_name="dataManagementCreateRetentionRules",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "retention_rules",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(DataManagementRuleInput),
                        graphql_name="retentionRules",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `retention_rules` (`[DataManagementRuleInput]`)
    """

    data_management_delete_event_retention_rule = sgqlc.types.Field(
        DataManagementRule,
        graphql_name="dataManagementDeleteEventRetentionRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "namespace",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="namespace",
                        default=None,
                    ),
                ),
            )
        ),
    )

    data_management_update_feature_settings = sgqlc.types.Field(
        DataManagementFeatureSetting,
        graphql_name="dataManagementUpdateFeatureSettings",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "setting",
                    sgqlc.types.Arg(
                        DataManagementAccountFeatureSettingInput,
                        graphql_name="setting",
                        default=None,
                    ),
                ),
            )
        ),
    )

    edge_create_trace_filter_rules = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeCreateTraceFilterRuleResponses),
        graphql_name="edgeCreateTraceFilterRules",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rules",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EdgeCreateTraceFilterRulesInput),
                        graphql_name="rules",
                        default=None,
                    ),
                ),
                (
                    "trace_observer_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="traceObserverId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    edge_create_trace_observer = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeCreateTraceObserverResponses),
        graphql_name="edgeCreateTraceObserver",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "trace_observer_configs",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(EdgeCreateTraceObserverInput)
                            )
                        ),
                        graphql_name="traceObserverConfigs",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `trace_observer_configs` (`[EdgeCreateTraceObserverInput!]!`)
    """

    edge_delete_trace_filter_rules = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeDeleteTraceFilterRuleResponses),
        graphql_name="edgeDeleteTraceFilterRules",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rules",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EdgeDeleteTraceFilterRulesInput),
                        graphql_name="rules",
                        default=None,
                    ),
                ),
                (
                    "trace_observer_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="traceObserverId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    edge_delete_trace_observers = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeDeleteTraceObserverResponses),
        graphql_name="edgeDeleteTraceObservers",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "trace_observer_configs",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(EdgeDeleteTraceObserverInput)
                            )
                        ),
                        graphql_name="traceObserverConfigs",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `trace_observer_configs` (`[EdgeDeleteTraceObserverInput!]!`)
    """

    edge_update_trace_observers = sgqlc.types.Field(
        sgqlc.types.non_null(EdgeUpdateTraceObserverResponses),
        graphql_name="edgeUpdateTraceObservers",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "trace_observer_configs",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(EdgeUpdateTraceObserverInput)
                            )
                        ),
                        graphql_name="traceObserverConfigs",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `trace_observer_configs` (`[EdgeUpdateTraceObserverInput!]!`)
    """

    entity_delete = sgqlc.types.Field(
        EntityDeleteResult,
        graphql_name="entityDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "force_delete",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="forceDelete",
                        default=False,
                    ),
                ),
                (
                    "guids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(EntityGuid))
                        ),
                        graphql_name="guids",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `force_delete` (`Boolean!`) (default: `false`)
    * `guids` (`[EntityGuid!]!`)
    """

    entity_golden_metrics_override = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenMetricsDomainTypeScopedResponse),
        graphql_name="entityGoldenMetricsOverride",
        args=sgqlc.types.ArgDict(
            (
                (
                    "context",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGoldenContextInput),
                        graphql_name="context",
                        default=None,
                    ),
                ),
                (
                    "domain_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(DomainTypeInput),
                        graphql_name="domainType",
                        default=None,
                    ),
                ),
                (
                    "metrics",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(EntityGoldenMetricInput)
                            )
                        ),
                        graphql_name="metrics",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `context` (`EntityGoldenContextInput!`)
    * `domain_type` (`DomainTypeInput!`)
    * `metrics` (`[EntityGoldenMetricInput!]!`)
    """

    entity_golden_metrics_reset = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenMetricsDomainTypeScopedResponse),
        graphql_name="entityGoldenMetricsReset",
        args=sgqlc.types.ArgDict(
            (
                (
                    "context",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGoldenContextInput),
                        graphql_name="context",
                        default=None,
                    ),
                ),
                (
                    "domain_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(DomainTypeInput),
                        graphql_name="domainType",
                        default=None,
                    ),
                ),
            )
        ),
    )

    entity_golden_tags_override = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenTagsDomainTypeScopedResponse),
        graphql_name="entityGoldenTagsOverride",
        args=sgqlc.types.ArgDict(
            (
                (
                    "context",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGoldenContextInput),
                        graphql_name="context",
                        default=None,
                    ),
                ),
                (
                    "domain_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(DomainTypeInput),
                        graphql_name="domainType",
                        default=None,
                    ),
                ),
                (
                    "tags",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(EntityGoldenTagInput)
                            )
                        ),
                        graphql_name="tags",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `context` (`EntityGoldenContextInput!`)
    * `domain_type` (`DomainTypeInput!`)
    * `tags` (`[EntityGoldenTagInput!]!`)
    """

    entity_golden_tags_reset = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGoldenTagsDomainTypeScopedResponse),
        graphql_name="entityGoldenTagsReset",
        args=sgqlc.types.ArgDict(
            (
                (
                    "context",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGoldenContextInput),
                        graphql_name="context",
                        default=None,
                    ),
                ),
                (
                    "domain_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(DomainTypeInput),
                        graphql_name="domainType",
                        default=None,
                    ),
                ),
            )
        ),
    )

    entity_relationship_user_defined_create_or_replace = sgqlc.types.Field(
        sgqlc.types.non_null(EntityRelationshipUserDefinedCreateOrReplaceResult),
        graphql_name="entityRelationshipUserDefinedCreateOrReplace",
        args=sgqlc.types.ArgDict(
            (
                (
                    "source_entity_guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="sourceEntityGuid",
                        default=None,
                    ),
                ),
                (
                    "target_entity_guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="targetEntityGuid",
                        default=None,
                    ),
                ),
                (
                    "type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityRelationshipEdgeType),
                        graphql_name="type",
                        default=None,
                    ),
                ),
            )
        ),
    )

    entity_relationship_user_defined_delete = sgqlc.types.Field(
        sgqlc.types.non_null(EntityRelationshipUserDefinedDeleteResult),
        graphql_name="entityRelationshipUserDefinedDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "source_entity_guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="sourceEntityGuid",
                        default=None,
                    ),
                ),
                (
                    "target_entity_guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="targetEntityGuid",
                        default=None,
                    ),
                ),
                (
                    "type",
                    sgqlc.types.Arg(
                        EntityRelationshipEdgeType, graphql_name="type", default=None
                    ),
                ),
            )
        ),
    )

    errors_inbox_assign_error_group = sgqlc.types.Field(
        ErrorsInboxAssignErrorGroupResponse,
        graphql_name="errorsInboxAssignErrorGroup",
        args=sgqlc.types.ArgDict(
            (
                (
                    "assignment",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ErrorsInboxAssignErrorGroupInput),
                        graphql_name="assignment",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    errors_inbox_delete_error_group_resource = sgqlc.types.Field(
        ErrorsInboxDeleteErrorGroupResourceResponse,
        graphql_name="errorsInboxDeleteErrorGroupResource",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
                (
                    "resource_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="resourceId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    errors_inbox_update_error_group_state = sgqlc.types.Field(
        ErrorsInboxUpdateErrorGroupStateResponse,
        graphql_name="errorsInboxUpdateErrorGroupState",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="ids",
                        default=None,
                    ),
                ),
                (
                    "state",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ErrorsInboxErrorGroupState),
                        graphql_name="state",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID`)
    * `ids` (`[ID!]`)
    * `state` (`ErrorsInboxErrorGroupState!`)
    """

    events_to_metrics_create_rule = sgqlc.types.Field(
        EventsToMetricsCreateRuleResult,
        graphql_name="eventsToMetricsCreateRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "rules",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(EventsToMetricsCreateRuleInput)
                        ),
                        graphql_name="rules",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `rules` (`[EventsToMetricsCreateRuleInput]!`)
    """

    events_to_metrics_delete_rule = sgqlc.types.Field(
        EventsToMetricsDeleteRuleResult,
        graphql_name="eventsToMetricsDeleteRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deletes",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(EventsToMetricsDeleteRuleInput)
                        ),
                        graphql_name="deletes",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `deletes` (`[EventsToMetricsDeleteRuleInput]!`)
    """

    events_to_metrics_update_rule = sgqlc.types.Field(
        EventsToMetricsUpdateRuleResult,
        graphql_name="eventsToMetricsUpdateRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "updates",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(EventsToMetricsUpdateRuleInput)
                        ),
                        graphql_name="updates",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `updates` (`[EventsToMetricsUpdateRuleInput]!`)
    """

    historical_data_export_cancel_export = sgqlc.types.Field(
        HistoricalDataExportCustomerExportResponse,
        graphql_name="historicalDataExportCancelExport",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    historical_data_export_create_export = sgqlc.types.Field(
        HistoricalDataExportCustomerExportResponse,
        graphql_name="historicalDataExportCreateExport",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                ("nrql", sgqlc.types.Arg(Nrql, graphql_name="nrql", default=None)),
            )
        ),
    )

    incident_intelligence_environment_consent_accounts = sgqlc.types.Field(
        IncidentIntelligenceEnvironmentConsentAccounts,
        graphql_name="incidentIntelligenceEnvironmentConsentAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(Int)),
                        graphql_name="accountIds",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_ids` (`[Int]!`)
    """

    incident_intelligence_environment_consent_authorized_accounts = sgqlc.types.Field(
        IncidentIntelligenceEnvironmentConsentAuthorizedAccounts,
        graphql_name="incidentIntelligenceEnvironmentConsentAuthorizedAccounts",
    )

    incident_intelligence_environment_delete_environment = sgqlc.types.Field(
        IncidentIntelligenceEnvironmentDeleteEnvironment,
        graphql_name="incidentIntelligenceEnvironmentDeleteEnvironment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    incident_intelligence_environment_dissent_accounts = sgqlc.types.Field(
        IncidentIntelligenceEnvironmentDissentAccounts,
        graphql_name="incidentIntelligenceEnvironmentDissentAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(Int)),
                        graphql_name="accountIds",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_ids` (`[Int]!`)
    """

    installation_create_install_status = sgqlc.types.Field(
        sgqlc.types.non_null(InstallationInstallStatus),
        graphql_name="installationCreateInstallStatus",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "install_status",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(InstallationInstallStatusInput),
                        graphql_name="installStatus",
                        default=None,
                    ),
                ),
            )
        ),
    )

    installation_create_recipe_event = sgqlc.types.Field(
        sgqlc.types.non_null(InstallationRecipeEvent),
        graphql_name="installationCreateRecipeEvent",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "status",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(InstallationRecipeStatus),
                        graphql_name="status",
                        default=None,
                    ),
                ),
            )
        ),
    )

    installation_delete_install = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="installationDeleteInstall",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    key_transaction_create = sgqlc.types.Field(
        KeyTransactionCreateResult,
        graphql_name="keyTransactionCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "apdex_target",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Float),
                        graphql_name="apdexTarget",
                        default=None,
                    ),
                ),
                (
                    "application_guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="applicationGuid",
                        default=None,
                    ),
                ),
                (
                    "browser_apdex_target",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Float),
                        graphql_name="browserApdexTarget",
                        default=None,
                    ),
                ),
                (
                    "metric_name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="metricName",
                        default=None,
                    ),
                ),
                (
                    "name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="name", default=None
                    ),
                ),
            )
        ),
    )

    key_transaction_delete = sgqlc.types.Field(
        KeyTransactionDeleteResult,
        graphql_name="keyTransactionDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    key_transaction_update = sgqlc.types.Field(
        KeyTransactionUpdateResult,
        graphql_name="keyTransactionUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "apdex_target",
                    sgqlc.types.Arg(Float, graphql_name="apdexTarget", default=None),
                ),
                (
                    "browser_apdex_target",
                    sgqlc.types.Arg(
                        Float, graphql_name="browserApdexTarget", default=None
                    ),
                ),
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                ("name", sgqlc.types.Arg(String, graphql_name="name", default=None)),
            )
        ),
    )

    log_configurations_create_data_partition_rule = sgqlc.types.Field(
        LogConfigurationsCreateDataPartitionRuleResponse,
        graphql_name="logConfigurationsCreateDataPartitionRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            LogConfigurationsCreateDataPartitionRuleInput
                        ),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    log_configurations_create_obfuscation_expression = sgqlc.types.Field(
        LogConfigurationsObfuscationExpression,
        graphql_name="logConfigurationsCreateObfuscationExpression",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "expression",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            LogConfigurationsCreateObfuscationExpressionInput
                        ),
                        graphql_name="expression",
                        default=None,
                    ),
                ),
            )
        ),
    )

    log_configurations_create_obfuscation_rule = sgqlc.types.Field(
        LogConfigurationsObfuscationRule,
        graphql_name="logConfigurationsCreateObfuscationRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            LogConfigurationsCreateObfuscationRuleInput
                        ),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    log_configurations_create_parsing_rule = sgqlc.types.Field(
        LogConfigurationsCreateParsingRuleResponse,
        graphql_name="logConfigurationsCreateParsingRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(LogConfigurationsParsingRuleConfiguration),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    log_configurations_delete_data_partition_rule = sgqlc.types.Field(
        LogConfigurationsDeleteDataPartitionRuleResponse,
        graphql_name="logConfigurationsDeleteDataPartitionRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    log_configurations_delete_obfuscation_expression = sgqlc.types.Field(
        LogConfigurationsObfuscationExpression,
        graphql_name="logConfigurationsDeleteObfuscationExpression",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    log_configurations_delete_obfuscation_rule = sgqlc.types.Field(
        LogConfigurationsObfuscationRule,
        graphql_name="logConfigurationsDeleteObfuscationRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    log_configurations_delete_parsing_rule = sgqlc.types.Field(
        LogConfigurationsDeleteParsingRuleResponse,
        graphql_name="logConfigurationsDeleteParsingRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    log_configurations_update_data_partition_rule = sgqlc.types.Field(
        LogConfigurationsUpdateDataPartitionRuleResponse,
        graphql_name="logConfigurationsUpdateDataPartitionRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        LogConfigurationsUpdateDataPartitionRuleInput,
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    log_configurations_update_obfuscation_expression = sgqlc.types.Field(
        LogConfigurationsObfuscationExpression,
        graphql_name="logConfigurationsUpdateObfuscationExpression",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "expression",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            LogConfigurationsUpdateObfuscationExpressionInput
                        ),
                        graphql_name="expression",
                        default=None,
                    ),
                ),
            )
        ),
    )

    log_configurations_update_obfuscation_rule = sgqlc.types.Field(
        LogConfigurationsObfuscationRule,
        graphql_name="logConfigurationsUpdateObfuscationRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            LogConfigurationsUpdateObfuscationRuleInput
                        ),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    log_configurations_update_parsing_rule = sgqlc.types.Field(
        LogConfigurationsUpdateParsingRuleResponse,
        graphql_name="logConfigurationsUpdateParsingRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(LogConfigurationsParsingRuleConfiguration),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    log_configurations_upsert_pipeline_configuration = sgqlc.types.Field(
        LogConfigurationsUpsertPipelineConfigurationResponse,
        graphql_name="logConfigurationsUpsertPipelineConfiguration",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "pipeline_configuration",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            LogConfigurationsPipelineConfigurationInput
                        ),
                        graphql_name="pipelineConfiguration",
                        default=None,
                    ),
                ),
            )
        ),
    )

    metric_normalization_create_rule = sgqlc.types.Field(
        MetricNormalizationRuleMutationResponse,
        graphql_name="metricNormalizationCreateRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetricNormalizationCreateRuleInput),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    metric_normalization_disable_rule = sgqlc.types.Field(
        MetricNormalizationRuleMutationResponse,
        graphql_name="metricNormalizationDisableRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name="ruleId", default=None
                    ),
                ),
            )
        ),
    )

    metric_normalization_edit_rule = sgqlc.types.Field(
        MetricNormalizationRuleMutationResponse,
        graphql_name="metricNormalizationEditRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(MetricNormalizationEditRuleInput),
                        graphql_name="rule",
                        default=None,
                    ),
                ),
            )
        ),
    )

    metric_normalization_enable_rule = sgqlc.types.Field(
        MetricNormalizationRuleMutationResponse,
        graphql_name="metricNormalizationEnableRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name="ruleId", default=None
                    ),
                ),
            )
        ),
    )

    mobile_push_notification_remove_device = sgqlc.types.Field(
        sgqlc.types.non_null(MobilePushNotificationRemoveDeviceResult),
        graphql_name="mobilePushNotificationRemoveDevice",
        args=sgqlc.types.ArgDict(
            (
                (
                    "device_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="deviceId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    mobile_push_notification_send_test_push = sgqlc.types.Field(
        sgqlc.types.non_null(MobilePushNotificationSendPushResult),
        graphql_name="mobilePushNotificationSendTestPush",
        args=sgqlc.types.ArgDict(
            (
                (
                    "device_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="deviceId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    mobile_push_notification_send_test_push_to_all = sgqlc.types.Field(
        sgqlc.types.non_null(MobilePushNotificationSendPushResult),
        graphql_name="mobilePushNotificationSendTestPushToAll",
    )

    nerd_storage_delete_collection = sgqlc.types.Field(
        NerdStorageDeleteResult,
        graphql_name="nerdStorageDeleteCollection",
        args=sgqlc.types.ArgDict(
            (
                (
                    "collection",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="collection",
                        default=None,
                    ),
                ),
                (
                    "scope",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdStorageScopeInput),
                        graphql_name="scope",
                        default=None,
                    ),
                ),
                (
                    "scope_by_actor",
                    sgqlc.types.Arg(Boolean, graphql_name="scopeByActor", default=None),
                ),
            )
        ),
    )

    nerd_storage_delete_document = sgqlc.types.Field(
        NerdStorageDeleteResult,
        graphql_name="nerdStorageDeleteDocument",
        args=sgqlc.types.ArgDict(
            (
                (
                    "collection",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="collection",
                        default=None,
                    ),
                ),
                (
                    "document_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="documentId",
                        default=None,
                    ),
                ),
                (
                    "scope",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdStorageScopeInput),
                        graphql_name="scope",
                        default=None,
                    ),
                ),
                (
                    "scope_by_actor",
                    sgqlc.types.Arg(Boolean, graphql_name="scopeByActor", default=None),
                ),
            )
        ),
    )

    nerd_storage_vault_delete_secret = sgqlc.types.Field(
        sgqlc.types.non_null(NerdStorageVaultDeleteSecretResult),
        graphql_name="nerdStorageVaultDeleteSecret",
        args=sgqlc.types.ArgDict(
            (
                (
                    "key",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="key", default=None
                    ),
                ),
                (
                    "scope",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdStorageVaultScope),
                        graphql_name="scope",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nerd_storage_vault_write_secret = sgqlc.types.Field(
        sgqlc.types.non_null(NerdStorageVaultWriteSecretResult),
        graphql_name="nerdStorageVaultWriteSecret",
        args=sgqlc.types.ArgDict(
            (
                (
                    "scope",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdStorageVaultScope),
                        graphql_name="scope",
                        default=None,
                    ),
                ),
                (
                    "secret",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdStorageVaultWriteSecretInput),
                        graphql_name="secret",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nerd_storage_write_document = sgqlc.types.Field(
        NerdStorageDocument,
        graphql_name="nerdStorageWriteDocument",
        args=sgqlc.types.ArgDict(
            (
                (
                    "collection",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="collection",
                        default=None,
                    ),
                ),
                (
                    "document",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdStorageDocument),
                        graphql_name="document",
                        default=None,
                    ),
                ),
                (
                    "document_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="documentId",
                        default=None,
                    ),
                ),
                (
                    "scope",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdStorageScopeInput),
                        graphql_name="scope",
                        default=None,
                    ),
                ),
                (
                    "scope_by_actor",
                    sgqlc.types.Arg(Boolean, graphql_name="scopeByActor", default=None),
                ),
            )
        ),
    )

    nerdpack_add_allowed_accounts = sgqlc.types.Field(
        NerdpackAllowListResult,
        graphql_name="nerdpackAddAllowedAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "allow_list",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdpackAllowListInput),
                        graphql_name="allowList",
                        default=None,
                    ),
                ),
                (
                    "nerdpack_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="nerdpackId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nerdpack_create = sgqlc.types.Field(
        sgqlc.types.non_null(NerdpackData),
        graphql_name="nerdpackCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "nerdpack_data",
                    sgqlc.types.Arg(
                        NerdpackCreationInput, graphql_name="nerdpackData", default=None
                    ),
                ),
            )
        ),
    )

    nerdpack_remove_allowed_accounts = sgqlc.types.Field(
        NerdpackAllowListResult,
        graphql_name="nerdpackRemoveAllowedAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "allow_list",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdpackAllowListInput),
                        graphql_name="allowList",
                        default=None,
                    ),
                ),
                (
                    "nerdpack_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="nerdpackId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nerdpack_remove_version_tag = sgqlc.types.Field(
        NerdpackRemovedTagResponse,
        graphql_name="nerdpackRemoveVersionTag",
        args=sgqlc.types.ArgDict(
            (
                (
                    "nerdpack_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="nerdpackId",
                        default=None,
                    ),
                ),
                (
                    "version_tag",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdpackRemoveVersionTagInput),
                        graphql_name="versionTag",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nerdpack_subscribe_accounts = sgqlc.types.Field(
        NerdpackSubscribeResult,
        graphql_name="nerdpackSubscribeAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "nerdpack_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="nerdpackId",
                        default=None,
                    ),
                ),
                (
                    "subscription",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdpackSubscribeAccountsInput),
                        graphql_name="subscription",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nerdpack_tag_version = sgqlc.types.Field(
        NerdpackVersion,
        graphql_name="nerdpackTagVersion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "nerdpack_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="nerdpackId",
                        default=None,
                    ),
                ),
                (
                    "version_tag",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdpackTagVersionInput),
                        graphql_name="versionTag",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nerdpack_unsubscribe_accounts = sgqlc.types.Field(
        NerdpackUnsubscribeResult,
        graphql_name="nerdpackUnsubscribeAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "nerdpack_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="nerdpackId",
                        default=None,
                    ),
                ),
                (
                    "subscription",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(NerdpackUnsubscribeAccountsInput),
                        graphql_name="subscription",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nr1_catalog_install_alert_policy_template = sgqlc.types.Field(
        Nr1CatalogInstallAlertPolicyTemplateResult,
        graphql_name="nr1CatalogInstallAlertPolicyTemplate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "alert_policy_template_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="alertPolicyTemplateId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nr1_catalog_install_dashboard_template = sgqlc.types.Field(
        Nr1CatalogInstallDashboardTemplateResult,
        graphql_name="nr1CatalogInstallDashboardTemplate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "dashboard_template_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID),
                        graphql_name="dashboardTemplateId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nr1_catalog_submit_metadata = sgqlc.types.Field(
        Nr1CatalogSubmitMetadataResult,
        graphql_name="nr1CatalogSubmitMetadata",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
                (
                    "nerdpack_metadata",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Nr1CatalogSubmitMetadataInput),
                        graphql_name="nerdpackMetadata",
                        default=None,
                    ),
                ),
            )
        ),
    )

    nrql_drop_rules_create = sgqlc.types.Field(
        NrqlDropRulesCreateDropRuleResult,
        graphql_name="nrqlDropRulesCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rules",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(NrqlDropRulesCreateDropRuleInput)
                        ),
                        graphql_name="rules",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `rules` (`[NrqlDropRulesCreateDropRuleInput]!`)
    """

    nrql_drop_rules_delete = sgqlc.types.Field(
        NrqlDropRulesDeleteDropRuleResult,
        graphql_name="nrqlDropRulesDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "rule_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(ID)),
                        graphql_name="ruleIds",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `rule_ids` (`[ID]!`)
    """

    organization_create_shared_account = sgqlc.types.Field(
        OrganizationCreateSharedAccountResponse,
        graphql_name="organizationCreateSharedAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "shared_account",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(OrganizationCreateSharedAccountInput),
                        graphql_name="sharedAccount",
                        default=None,
                    ),
                ),
            )
        ),
    )

    organization_provisioning_update_partner_subscription = sgqlc.types.Field(
        sgqlc.types.non_null(OrganizationProvisioningUpdateSubscriptionResult),
        graphql_name="organizationProvisioningUpdatePartnerSubscription",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "affected_account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="affectedAccountId",
                        default=None,
                    ),
                ),
                (
                    "products",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(
                                    OrganizationProvisioningProductInput
                                )
                            )
                        ),
                        graphql_name="products",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `account_id` (`Int!`)
    * `affected_account_id` (`Int!`)
    * `products` (`[OrganizationProvisioningProductInput!]!`)
    """

    organization_revoke_shared_account = sgqlc.types.Field(
        OrganizationRevokeSharedAccountResponse,
        graphql_name="organizationRevokeSharedAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "shared_account",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(OrganizationRevokeSharedAccountInput),
                        graphql_name="sharedAccount",
                        default=None,
                    ),
                ),
            )
        ),
    )

    organization_update = sgqlc.types.Field(
        OrganizationUpdateResponse,
        graphql_name="organizationUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "organization",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(OrganizationUpdateInput),
                        graphql_name="organization",
                        default=None,
                    ),
                ),
                (
                    "organization_id",
                    sgqlc.types.Arg(ID, graphql_name="organizationId", default=None),
                ),
            )
        ),
    )

    organization_update_shared_account = sgqlc.types.Field(
        OrganizationUpdateSharedAccountResponse,
        graphql_name="organizationUpdateSharedAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "shared_account",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(OrganizationUpdateSharedAccountInput),
                        graphql_name="sharedAccount",
                        default=None,
                    ),
                ),
            )
        ),
    )

    pixie_link_pixie_project = sgqlc.types.Field(
        PixieLinkPixieProjectResult,
        graphql_name="pixieLinkPixieProject",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "api_key",
                    sgqlc.types.Arg(SecureValue, graphql_name="apiKey", default=None),
                ),
            )
        ),
    )

    pixie_record_pixie_tos_acceptance = sgqlc.types.Field(
        PixieRecordPixieTosAcceptanceResult,
        graphql_name="pixieRecordPixieTosAcceptance",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    pixie_unlink_pixie_project = sgqlc.types.Field(
        PixieLinkPixieProjectResult,
        graphql_name="pixieUnlinkPixieProject",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    reference_entity_create_or_update_repository = sgqlc.types.Field(
        ReferenceEntityCreateRepositoryResult,
        graphql_name="referenceEntityCreateOrUpdateRepository",
        args=sgqlc.types.ArgDict(
            (
                (
                    "repositories",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(
                                    ReferenceEntityCreateRepositoryInput
                                )
                            )
                        ),
                        graphql_name="repositories",
                        default=None,
                    ),
                ),
                ("sync", sgqlc.types.Arg(Boolean, graphql_name="sync", default=None)),
            )
        ),
    )
    """Arguments:

    * `repositories` (`[ReferenceEntityCreateRepositoryInput!]!`)
    * `sync` (`Boolean`)
    """

    service_level_create = sgqlc.types.Field(
        "ServiceLevelIndicator",
        graphql_name="serviceLevelCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "entity_guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="entityGuid",
                        default=None,
                    ),
                ),
                (
                    "indicator",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ServiceLevelIndicatorCreateInput),
                        graphql_name="indicator",
                        default=None,
                    ),
                ),
            )
        ),
    )

    service_level_delete = sgqlc.types.Field(
        "ServiceLevelIndicator",
        graphql_name="serviceLevelDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(EntityGuid, graphql_name="guid", default=None),
                ),
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
            )
        ),
    )

    service_level_update = sgqlc.types.Field(
        "ServiceLevelIndicator",
        graphql_name="serviceLevelUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(EntityGuid, graphql_name="guid", default=None),
                ),
                ("id", sgqlc.types.Arg(ID, graphql_name="id", default=None)),
                (
                    "indicator",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ServiceLevelIndicatorUpdateInput),
                        graphql_name="indicator",
                        default=None,
                    ),
                ),
            )
        ),
    )

    streaming_export_create_rule = sgqlc.types.Field(
        "StreamingExportRule",
        graphql_name="streamingExportCreateRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "aws_parameters",
                    sgqlc.types.Arg(
                        StreamingExportAwsInput,
                        graphql_name="awsParameters",
                        default=None,
                    ),
                ),
                (
                    "azure_parameters",
                    sgqlc.types.Arg(
                        StreamingExportAzureInput,
                        graphql_name="azureParameters",
                        default=None,
                    ),
                ),
                (
                    "rule_parameters",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(StreamingExportRuleInput),
                        graphql_name="ruleParameters",
                        default=None,
                    ),
                ),
            )
        ),
    )

    streaming_export_delete_rule = sgqlc.types.Field(
        "StreamingExportRule",
        graphql_name="streamingExportDeleteRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    streaming_export_disable_rule = sgqlc.types.Field(
        "StreamingExportRule",
        graphql_name="streamingExportDisableRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    streaming_export_enable_rule = sgqlc.types.Field(
        "StreamingExportRule",
        graphql_name="streamingExportEnableRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    streaming_export_update_rule = sgqlc.types.Field(
        "StreamingExportRule",
        graphql_name="streamingExportUpdateRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "aws_parameters",
                    sgqlc.types.Arg(
                        StreamingExportAwsInput,
                        graphql_name="awsParameters",
                        default=None,
                    ),
                ),
                (
                    "azure_parameters",
                    sgqlc.types.Arg(
                        StreamingExportAzureInput,
                        graphql_name="azureParameters",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
                (
                    "rule_parameters",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(StreamingExportRuleInput),
                        graphql_name="ruleParameters",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_create_broken_links_monitor = sgqlc.types.Field(
        "SyntheticsBrokenLinksMonitorCreateMutationResult",
        graphql_name="syntheticsCreateBrokenLinksMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsCreateBrokenLinksMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_create_cert_check_monitor = sgqlc.types.Field(
        "SyntheticsCertCheckMonitorCreateMutationResult",
        graphql_name="syntheticsCreateCertCheckMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsCreateCertCheckMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_create_private_location = sgqlc.types.Field(
        "SyntheticsPrivateLocationMutationResult",
        graphql_name="syntheticsCreatePrivateLocation",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="name", default=None
                    ),
                ),
                (
                    "verified_script_execution",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="verifiedScriptExecution",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_create_script_api_monitor = sgqlc.types.Field(
        "SyntheticsScriptApiMonitorCreateMutationResult",
        graphql_name="syntheticsCreateScriptApiMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsCreateScriptApiMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_create_script_browser_monitor = sgqlc.types.Field(
        "SyntheticsScriptBrowserMonitorCreateMutationResult",
        graphql_name="syntheticsCreateScriptBrowserMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsCreateScriptBrowserMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_create_secure_credential = sgqlc.types.Field(
        "SyntheticsSecureCredentialMutationResult",
        graphql_name="syntheticsCreateSecureCredential",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "key",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="key", default=None
                    ),
                ),
                (
                    "value",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SecureValue),
                        graphql_name="value",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_create_simple_browser_monitor = sgqlc.types.Field(
        "SyntheticsSimpleBrowserMonitorCreateMutationResult",
        graphql_name="syntheticsCreateSimpleBrowserMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsCreateSimpleBrowserMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_create_simple_monitor = sgqlc.types.Field(
        "SyntheticsSimpleBrowserMonitorCreateMutationResult",
        graphql_name="syntheticsCreateSimpleMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsCreateSimpleMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_create_step_monitor = sgqlc.types.Field(
        "SyntheticsStepMonitorCreateMutationResult",
        graphql_name="syntheticsCreateStepMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsCreateStepMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_delete_monitor = sgqlc.types.Field(
        "SyntheticsMonitorDeleteMutationResult",
        graphql_name="syntheticsDeleteMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_delete_private_location = sgqlc.types.Field(
        "SyntheticsPrivateLocationDeleteResult",
        graphql_name="syntheticsDeletePrivateLocation",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_delete_secure_credential = sgqlc.types.Field(
        "SyntheticsSecureCredentialMutationResult",
        graphql_name="syntheticsDeleteSecureCredential",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "key",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="key", default=None
                    ),
                ),
            )
        ),
    )

    synthetics_purge_private_location_queue = sgqlc.types.Field(
        "SyntheticsPrivateLocationPurgeQueueResult",
        graphql_name="syntheticsPurgePrivateLocationQueue",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_update_broken_links_monitor = sgqlc.types.Field(
        "SyntheticsBrokenLinksMonitorUpdateMutationResult",
        graphql_name="syntheticsUpdateBrokenLinksMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsUpdateBrokenLinksMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_update_cert_check_monitor = sgqlc.types.Field(
        "SyntheticsCertCheckMonitorUpdateMutationResult",
        graphql_name="syntheticsUpdateCertCheckMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsUpdateCertCheckMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_update_private_location = sgqlc.types.Field(
        "SyntheticsPrivateLocationMutationResult",
        graphql_name="syntheticsUpdatePrivateLocation",
        args=sgqlc.types.ArgDict(
            (
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "verified_script_execution",
                    sgqlc.types.Arg(
                        Boolean, graphql_name="verifiedScriptExecution", default=None
                    ),
                ),
            )
        ),
    )

    synthetics_update_script_api_monitor = sgqlc.types.Field(
        "SyntheticsScriptApiMonitorUpdateMutationResult",
        graphql_name="syntheticsUpdateScriptApiMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsUpdateScriptApiMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_update_script_browser_monitor = sgqlc.types.Field(
        "SyntheticsScriptBrowserMonitorUpdateMutationResult",
        graphql_name="syntheticsUpdateScriptBrowserMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsUpdateScriptBrowserMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_update_secure_credential = sgqlc.types.Field(
        "SyntheticsSecureCredentialMutationResult",
        graphql_name="syntheticsUpdateSecureCredential",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "key",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="key", default=None
                    ),
                ),
                (
                    "value",
                    sgqlc.types.Arg(SecureValue, graphql_name="value", default=None),
                ),
            )
        ),
    )

    synthetics_update_simple_browser_monitor = sgqlc.types.Field(
        "SyntheticsSimpleBrowserMonitorUpdateMutationResult",
        graphql_name="syntheticsUpdateSimpleBrowserMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsUpdateSimpleBrowserMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_update_simple_monitor = sgqlc.types.Field(
        "SyntheticsSimpleMonitorUpdateMutationResult",
        graphql_name="syntheticsUpdateSimpleMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsUpdateSimpleMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    synthetics_update_step_monitor = sgqlc.types.Field(
        "SyntheticsStepMonitorUpdateMutationResult",
        graphql_name="syntheticsUpdateStepMonitor",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "monitor",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(SyntheticsUpdateStepMonitorInput),
                        graphql_name="monitor",
                        default=None,
                    ),
                ),
            )
        ),
    )

    tagging_add_tags_to_entity = sgqlc.types.Field(
        "TaggingMutationResult",
        graphql_name="taggingAddTagsToEntity",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "tags",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(TaggingTagInput))
                        ),
                        graphql_name="tags",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `guid` (`EntityGuid!`)
    * `tags` (`[TaggingTagInput!]!`)
    """

    tagging_delete_tag_from_entity = sgqlc.types.Field(
        "TaggingMutationResult",
        graphql_name="taggingDeleteTagFromEntity",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "tag_keys",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(String))
                        ),
                        graphql_name="tagKeys",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `guid` (`EntityGuid!`)
    * `tag_keys` (`[String!]!`)
    """

    tagging_delete_tag_values_from_entity = sgqlc.types.Field(
        "TaggingMutationResult",
        graphql_name="taggingDeleteTagValuesFromEntity",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "tag_values",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(
                                sgqlc.types.non_null(TaggingTagValueInput)
                            )
                        ),
                        graphql_name="tagValues",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `guid` (`EntityGuid!`)
    * `tag_values` (`[TaggingTagValueInput!]!`)
    """

    tagging_replace_tags_on_entity = sgqlc.types.Field(
        "TaggingMutationResult",
        graphql_name="taggingReplaceTagsOnEntity",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "tags",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(sgqlc.types.non_null(TaggingTagInput))
                        ),
                        graphql_name="tags",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `guid` (`EntityGuid!`)
    * `tags` (`[TaggingTagInput!]!`)
    """

    user_management_add_users_to_groups = sgqlc.types.Field(
        "UserManagementAddUsersToGroupsPayload",
        graphql_name="userManagementAddUsersToGroups",
        args=sgqlc.types.ArgDict(
            (
                (
                    "add_users_to_groups_options",
                    sgqlc.types.Arg(
                        UserManagementUsersGroupsInput,
                        graphql_name="addUsersToGroupsOptions",
                        default=None,
                    ),
                ),
            )
        ),
    )

    user_management_create_group = sgqlc.types.Field(
        "UserManagementCreateGroupPayload",
        graphql_name="userManagementCreateGroup",
        args=sgqlc.types.ArgDict(
            (
                (
                    "create_group_options",
                    sgqlc.types.Arg(
                        UserManagementCreateGroup,
                        graphql_name="createGroupOptions",
                        default=None,
                    ),
                ),
            )
        ),
    )

    user_management_create_user = sgqlc.types.Field(
        "UserManagementCreateUserPayload",
        graphql_name="userManagementCreateUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "create_user_options",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(UserManagementCreateUser),
                        graphql_name="createUserOptions",
                        default=None,
                    ),
                ),
            )
        ),
    )

    user_management_delete_group = sgqlc.types.Field(
        "UserManagementDeleteGroupPayload",
        graphql_name="userManagementDeleteGroup",
        args=sgqlc.types.ArgDict(
            (
                (
                    "group_options",
                    sgqlc.types.Arg(
                        UserManagementDeleteGroup,
                        graphql_name="groupOptions",
                        default=None,
                    ),
                ),
            )
        ),
    )

    user_management_delete_user = sgqlc.types.Field(
        "UserManagementDeleteUserPayload",
        graphql_name="userManagementDeleteUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "delete_user_options",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(UserManagementDeleteUser),
                        graphql_name="deleteUserOptions",
                        default=None,
                    ),
                ),
            )
        ),
    )

    user_management_remove_users_from_groups = sgqlc.types.Field(
        "UserManagementRemoveUsersFromGroupsPayload",
        graphql_name="userManagementRemoveUsersFromGroups",
        args=sgqlc.types.ArgDict(
            (
                (
                    "remove_users_from_groups_options",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(UserManagementUsersGroupsInput),
                        graphql_name="removeUsersFromGroupsOptions",
                        default=None,
                    ),
                ),
            )
        ),
    )

    user_management_update_group = sgqlc.types.Field(
        "UserManagementUpdateGroupPayload",
        graphql_name="userManagementUpdateGroup",
        args=sgqlc.types.ArgDict(
            (
                (
                    "update_group_options",
                    sgqlc.types.Arg(
                        UserManagementUpdateGroup,
                        graphql_name="updateGroupOptions",
                        default=None,
                    ),
                ),
            )
        ),
    )

    user_management_update_user = sgqlc.types.Field(
        "UserManagementUpdateUserPayload",
        graphql_name="userManagementUpdateUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "update_user_options",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(UserManagementUpdateUser),
                        graphql_name="updateUserOptions",
                        default=None,
                    ),
                ),
            )
        ),
    )

    whats_new_set_last_read_date = sgqlc.types.Field(
        EpochMilliseconds,
        graphql_name="whatsNewSetLastReadDate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "date",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EpochMilliseconds),
                        graphql_name="date",
                        default=None,
                    ),
                ),
            )
        ),
    )

    workload_create = sgqlc.types.Field(
        "WorkloadCollection",
        graphql_name="workloadCreate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "workload",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkloadCreateInput),
                        graphql_name="workload",
                        default=None,
                    ),
                ),
            )
        ),
    )

    workload_delete = sgqlc.types.Field(
        "WorkloadCollection",
        graphql_name="workloadDelete",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    workload_duplicate = sgqlc.types.Field(
        "WorkloadCollection",
        graphql_name="workloadDuplicate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "account_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="accountId",
                        default=None,
                    ),
                ),
                (
                    "source_guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="sourceGuid",
                        default=None,
                    ),
                ),
                (
                    "workload",
                    sgqlc.types.Arg(
                        WorkloadDuplicateInput, graphql_name="workload", default=None
                    ),
                ),
            )
        ),
    )

    workload_update = sgqlc.types.Field(
        "WorkloadCollection",
        graphql_name="workloadUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="guid",
                        default=None,
                    ),
                ),
                (
                    "workload",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(WorkloadUpdateInput),
                        graphql_name="workload",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `guid` (`EntityGuid!`)
    * `workload` (`WorkloadUpdateInput!`)
    """


class RootQueryType(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("actor", "docs", "request_context")
    actor = sgqlc.types.Field(Actor, graphql_name="actor")

    docs = sgqlc.types.Field(DocumentationFields, graphql_name="docs")

    request_context = sgqlc.types.Field(RequestContext, graphql_name="requestContext")


class SecureCredentialSummaryData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ()


class ServiceLevelDefinition(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("indicators",)
    indicators = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("ServiceLevelIndicator")),
        graphql_name="indicators",
    )


class ServiceLevelEvents(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account", "bad_events", "good_events", "valid_events")
    account = sgqlc.types.Field(AccountReference, graphql_name="account")

    bad_events = sgqlc.types.Field("ServiceLevelEventsQuery", graphql_name="badEvents")

    good_events = sgqlc.types.Field(
        "ServiceLevelEventsQuery", graphql_name="goodEvents"
    )

    valid_events = sgqlc.types.Field(
        sgqlc.types.non_null("ServiceLevelEventsQuery"), graphql_name="validEvents"
    )


class ServiceLevelEventsQuery(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("from_", "select", "where")
    from_ = sgqlc.types.Field(sgqlc.types.non_null(Nrql), graphql_name="from")

    select = sgqlc.types.Field("ServiceLevelEventsQuerySelect", graphql_name="select")

    where = sgqlc.types.Field(Nrql, graphql_name="where")


class ServiceLevelEventsQuerySelect(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attribute", "function", "threshold")
    attribute = sgqlc.types.Field(String, graphql_name="attribute")

    function = sgqlc.types.Field(
        sgqlc.types.non_null(ServiceLevelEventsQuerySelectFunction),
        graphql_name="function",
    )

    threshold = sgqlc.types.Field(Float, graphql_name="threshold")


class ServiceLevelIndicator(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "created_by",
        "description",
        "entity_guid",
        "events",
        "guid",
        "id",
        "name",
        "objectives",
        "result_queries",
        "updated_at",
        "updated_by",
    )
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    created_by = sgqlc.types.Field("UserReference", graphql_name="createdBy")

    description = sgqlc.types.Field(String, graphql_name="description")

    entity_guid = sgqlc.types.Field(
        sgqlc.types.non_null(EntityGuid), graphql_name="entityGuid"
    )

    events = sgqlc.types.Field(
        sgqlc.types.non_null(ServiceLevelEvents), graphql_name="events"
    )

    guid = sgqlc.types.Field(sgqlc.types.non_null(EntityGuid), graphql_name="guid")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    objectives = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("ServiceLevelObjective")),
        graphql_name="objectives",
    )

    result_queries = sgqlc.types.Field(
        "ServiceLevelIndicatorResultQueries", graphql_name="resultQueries"
    )

    updated_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="updatedAt")

    updated_by = sgqlc.types.Field("UserReference", graphql_name="updatedBy")


class ServiceLevelIndicatorResultQueries(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("good_events", "indicator", "valid_events")
    good_events = sgqlc.types.Field(
        sgqlc.types.non_null("ServiceLevelResultQuery"), graphql_name="goodEvents"
    )

    indicator = sgqlc.types.Field(
        sgqlc.types.non_null("ServiceLevelResultQuery"), graphql_name="indicator"
    )

    valid_events = sgqlc.types.Field(
        sgqlc.types.non_null("ServiceLevelResultQuery"), graphql_name="validEvents"
    )


class ServiceLevelObjective(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "name", "result_queries", "target", "time_window")
    description = sgqlc.types.Field(String, graphql_name="description")

    name = sgqlc.types.Field(String, graphql_name="name")

    result_queries = sgqlc.types.Field(
        "ServiceLevelObjectiveResultQueries", graphql_name="resultQueries"
    )

    target = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name="target")

    time_window = sgqlc.types.Field(
        sgqlc.types.non_null("ServiceLevelObjectiveTimeWindow"),
        graphql_name="timeWindow",
    )


class ServiceLevelObjectiveResultQueries(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("attainment",)
    attainment = sgqlc.types.Field(
        sgqlc.types.non_null("ServiceLevelResultQuery"), graphql_name="attainment"
    )


class ServiceLevelObjectiveRollingTimeWindow(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("count", "unit")
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="count")

    unit = sgqlc.types.Field(
        sgqlc.types.non_null(ServiceLevelObjectiveRollingTimeWindowUnit),
        graphql_name="unit",
    )


class ServiceLevelObjectiveTimeWindow(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("rolling",)
    rolling = sgqlc.types.Field(
        ServiceLevelObjectiveRollingTimeWindow, graphql_name="rolling"
    )


class ServiceLevelResultQuery(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("nrql",)
    nrql = sgqlc.types.Field(sgqlc.types.non_null(Nrql), graphql_name="nrql")


class StackTraceApmException(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "stack_trace")
    message = sgqlc.types.Field(String, graphql_name="message")

    stack_trace = sgqlc.types.Field(
        "StackTraceApmStackTrace", graphql_name="stackTrace"
    )


class StackTraceApmStackTrace(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("frames",)
    frames = sgqlc.types.Field(
        sgqlc.types.list_of("StackTraceApmStackTraceFrame"), graphql_name="frames"
    )


class StackTraceApmStackTraceFrame(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("filepath", "formatted", "line", "name")
    filepath = sgqlc.types.Field(String, graphql_name="filepath")

    formatted = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="formatted"
    )

    line = sgqlc.types.Field(Int, graphql_name="line")

    name = sgqlc.types.Field(String, graphql_name="name")


class StackTraceBrowserException(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "stack_trace")
    message = sgqlc.types.Field(String, graphql_name="message")

    stack_trace = sgqlc.types.Field(
        "StackTraceBrowserStackTrace", graphql_name="stackTrace"
    )


class StackTraceBrowserStackTrace(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("frames",)
    frames = sgqlc.types.Field(
        sgqlc.types.list_of("StackTraceBrowserStackTraceFrame"), graphql_name="frames"
    )


class StackTraceBrowserStackTraceFrame(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("column", "formatted", "line", "name")
    column = sgqlc.types.Field(Int, graphql_name="column")

    formatted = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="formatted"
    )

    line = sgqlc.types.Field(Int, graphql_name="line")

    name = sgqlc.types.Field(String, graphql_name="name")


class StackTraceMobileCrash(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("stack_trace",)
    stack_trace = sgqlc.types.Field(
        "StackTraceMobileCrashStackTrace", graphql_name="stackTrace"
    )


class StackTraceMobileCrashStackTrace(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("frames",)
    frames = sgqlc.types.Field(
        sgqlc.types.list_of("StackTraceMobileCrashStackTraceFrame"),
        graphql_name="frames",
    )


class StackTraceMobileCrashStackTraceFrame(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("filepath", "formatted", "line", "name")
    filepath = sgqlc.types.Field(String, graphql_name="filepath")

    formatted = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="formatted"
    )

    line = sgqlc.types.Field(Int, graphql_name="line")

    name = sgqlc.types.Field(String, graphql_name="name")


class StackTraceMobileException(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("stack_trace",)
    stack_trace = sgqlc.types.Field(
        "StackTraceMobileExceptionStackTrace", graphql_name="stackTrace"
    )


class StackTraceMobileExceptionStackTrace(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("frames",)
    frames = sgqlc.types.Field(
        sgqlc.types.list_of("StackTraceMobileExceptionStackTraceFrame"),
        graphql_name="frames",
    )


class StackTraceMobileExceptionStackTraceFrame(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("filepath", "formatted", "line", "name")
    filepath = sgqlc.types.Field(String, graphql_name="filepath")

    formatted = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="formatted"
    )

    line = sgqlc.types.Field(Int, graphql_name="line")

    name = sgqlc.types.Field(String, graphql_name="name")


class StreamingExportAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("streaming_rule", "streaming_rules")
    streaming_rule = sgqlc.types.Field(
        "StreamingExportRule",
        graphql_name="streamingRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    streaming_rules = sgqlc.types.Field(
        sgqlc.types.list_of("StreamingExportRule"), graphql_name="streamingRules"
    )


class StreamingExportAwsDetails(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("aws_account_id", "delivery_stream_name", "region", "role")
    aws_account_id = sgqlc.types.Field(
        sgqlc.types.non_null(ID), graphql_name="awsAccountId"
    )

    delivery_stream_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="deliveryStreamName"
    )

    region = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="region")

    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="role")


class StreamingExportAzureDetails(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("event_hub_connection_string", "event_hub_name")
    event_hub_connection_string = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="eventHubConnectionString"
    )

    event_hub_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="eventHubName"
    )


class StreamingExportRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account",
        "aws",
        "azure",
        "created_at",
        "description",
        "id",
        "message",
        "name",
        "nrql",
        "status",
        "updated_at",
    )
    account = sgqlc.types.Field(AccountReference, graphql_name="account")

    aws = sgqlc.types.Field(StreamingExportAwsDetails, graphql_name="aws")

    azure = sgqlc.types.Field(StreamingExportAzureDetails, graphql_name="azure")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    message = sgqlc.types.Field(String, graphql_name="message")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    nrql = sgqlc.types.Field(Nrql, graphql_name="nrql")

    status = sgqlc.types.Field(
        sgqlc.types.non_null(StreamingExportStatus), graphql_name="status"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="updatedAt"
    )


class SuggestedNrqlQueryAnomaly(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("time_window",)
    time_window = sgqlc.types.Field(
        sgqlc.types.non_null("TimeWindow"), graphql_name="timeWindow"
    )


class SuggestedNrqlQueryResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("suggestions",)
    suggestions = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(SuggestedNrqlQuery)),
        graphql_name="suggestions",
    )


class SyntheticMonitorSummaryData(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "locations_failing",
        "locations_running",
        "status",
        "success_rate",
    )
    locations_failing = sgqlc.types.Field(Int, graphql_name="locationsFailing")

    locations_running = sgqlc.types.Field(Int, graphql_name="locationsRunning")

    status = sgqlc.types.Field(SyntheticMonitorStatus, graphql_name="status")

    success_rate = sgqlc.types.Field(Float, graphql_name="successRate")


class SyntheticsAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("script", "steps")
    script = sgqlc.types.Field(
        "SyntheticsMonitorScriptQueryResponse",
        graphql_name="script",
        args=sgqlc.types.ArgDict(
            (
                (
                    "monitor_guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="monitorGuid",
                        default=None,
                    ),
                ),
            )
        ),
    )

    steps = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("SyntheticsStep")),
        graphql_name="steps",
        args=sgqlc.types.ArgDict(
            (
                (
                    "monitor_guid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityGuid),
                        graphql_name="monitorGuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `monitor_guid` (`EntityGuid!`)
    """


class SyntheticsBrokenLinksMonitor(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "guid",
        "id",
        "locations",
        "modified_at",
        "name",
        "period",
        "status",
        "uri",
    )
    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    id = sgqlc.types.Field(ID, graphql_name="id")

    locations = sgqlc.types.Field("SyntheticsLocations", graphql_name="locations")

    modified_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="modifiedAt")

    name = sgqlc.types.Field(String, graphql_name="name")

    period = sgqlc.types.Field(SyntheticsMonitorPeriod, graphql_name="period")

    status = sgqlc.types.Field(SyntheticsMonitorStatus, graphql_name="status")

    uri = sgqlc.types.Field(String, graphql_name="uri")


class SyntheticsBrokenLinksMonitorCreateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of("SyntheticsMonitorCreateError")),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsBrokenLinksMonitor, graphql_name="monitor")


class SyntheticsBrokenLinksMonitorUpdateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of("SyntheticsMonitorUpdateError")),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsBrokenLinksMonitor, graphql_name="monitor")


class SyntheticsCertCheckMonitor(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "domain",
        "guid",
        "id",
        "locations",
        "modified_at",
        "name",
        "number_days_to_fail_before_cert_expires",
        "period",
        "status",
    )
    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    domain = sgqlc.types.Field(String, graphql_name="domain")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    id = sgqlc.types.Field(ID, graphql_name="id")

    locations = sgqlc.types.Field("SyntheticsLocations", graphql_name="locations")

    modified_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="modifiedAt")

    name = sgqlc.types.Field(String, graphql_name="name")

    number_days_to_fail_before_cert_expires = sgqlc.types.Field(
        Int, graphql_name="numberDaysToFailBeforeCertExpires"
    )

    period = sgqlc.types.Field(SyntheticsMonitorPeriod, graphql_name="period")

    status = sgqlc.types.Field(SyntheticsMonitorStatus, graphql_name="status")


class SyntheticsCertCheckMonitorCreateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of("SyntheticsMonitorCreateError")),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsCertCheckMonitor, graphql_name="monitor")


class SyntheticsCertCheckMonitorUpdateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of("SyntheticsMonitorUpdateError")),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsCertCheckMonitor, graphql_name="monitor")


class SyntheticsCustomHeader(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class SyntheticsDeviceEmulation(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("device_orientation", "device_type")
    device_orientation = sgqlc.types.Field(
        sgqlc.types.non_null(SyntheticsDeviceOrientation),
        graphql_name="deviceOrientation",
    )

    device_type = sgqlc.types.Field(
        sgqlc.types.non_null(SyntheticsDeviceType), graphql_name="deviceType"
    )


class SyntheticsError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description",)
    description = sgqlc.types.Field(String, graphql_name="description")


class SyntheticsLocations(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("private", "public")
    private = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="private")

    public = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="public")


class SyntheticsMonitorCreateError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(SyntheticsMonitorCreateErrorType), graphql_name="type"
    )


class SyntheticsMonitorDeleteMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("deleted_guid",)
    deleted_guid = sgqlc.types.Field(EntityGuid, graphql_name="deletedGuid")


class SyntheticsMonitorScriptQueryResponse(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("text",)
    text = sgqlc.types.Field(String, graphql_name="text")


class SyntheticsMonitorUpdateError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(SyntheticsMonitorUpdateErrorType), graphql_name="type"
    )


class SyntheticsPrivateLocationDeleteResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of("SyntheticsPrivateLocationMutationError"),
        graphql_name="errors",
    )


class SyntheticsPrivateLocationMutationError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "type")
    description = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="description"
    )

    type = sgqlc.types.Field(
        sgqlc.types.non_null(SyntheticsPrivateLocationMutationErrorType),
        graphql_name="type",
    )


class SyntheticsPrivateLocationMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account_id",
        "description",
        "domain_id",
        "errors",
        "guid",
        "key",
        "location_id",
        "name",
        "verified_script_execution",
    )
    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    description = sgqlc.types.Field(String, graphql_name="description")

    domain_id = sgqlc.types.Field(String, graphql_name="domainId")

    errors = sgqlc.types.Field(
        sgqlc.types.list_of(SyntheticsPrivateLocationMutationError),
        graphql_name="errors",
    )

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    key = sgqlc.types.Field(String, graphql_name="key")

    location_id = sgqlc.types.Field(String, graphql_name="locationId")

    name = sgqlc.types.Field(String, graphql_name="name")

    verified_script_execution = sgqlc.types.Field(
        Boolean, graphql_name="verifiedScriptExecution"
    )


class SyntheticsPrivateLocationPurgeQueueResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(SyntheticsPrivateLocationMutationError),
        graphql_name="errors",
    )


class SyntheticsRuntime(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("runtime_type", "runtime_type_version", "script_language")
    runtime_type = sgqlc.types.Field(String, graphql_name="runtimeType")

    runtime_type_version = sgqlc.types.Field(
        sgqlc.types.non_null(SemVer), graphql_name="runtimeTypeVersion"
    )

    script_language = sgqlc.types.Field(String, graphql_name="scriptLanguage")


class SyntheticsScriptApiMonitor(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "guid",
        "id",
        "locations",
        "modified_at",
        "name",
        "period",
        "runtime",
        "status",
    )
    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    id = sgqlc.types.Field(ID, graphql_name="id")

    locations = sgqlc.types.Field(SyntheticsLocations, graphql_name="locations")

    modified_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="modifiedAt")

    name = sgqlc.types.Field(String, graphql_name="name")

    period = sgqlc.types.Field(SyntheticsMonitorPeriod, graphql_name="period")

    runtime = sgqlc.types.Field(SyntheticsRuntime, graphql_name="runtime")

    status = sgqlc.types.Field(SyntheticsMonitorStatus, graphql_name="status")


class SyntheticsScriptApiMonitorCreateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(SyntheticsMonitorCreateError)),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsScriptApiMonitor, graphql_name="monitor")


class SyntheticsScriptApiMonitorUpdateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(SyntheticsMonitorUpdateError)),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsScriptApiMonitor, graphql_name="monitor")


class SyntheticsScriptBrowserMonitor(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "advanced_options",
        "created_at",
        "guid",
        "id",
        "locations",
        "modified_at",
        "name",
        "period",
        "runtime",
        "status",
    )
    advanced_options = sgqlc.types.Field(
        "SyntheticsScriptBrowserMonitorAdvancedOptions", graphql_name="advancedOptions"
    )

    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    id = sgqlc.types.Field(ID, graphql_name="id")

    locations = sgqlc.types.Field(SyntheticsLocations, graphql_name="locations")

    modified_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="modifiedAt")

    name = sgqlc.types.Field(String, graphql_name="name")

    period = sgqlc.types.Field(SyntheticsMonitorPeriod, graphql_name="period")

    runtime = sgqlc.types.Field(SyntheticsRuntime, graphql_name="runtime")

    status = sgqlc.types.Field(SyntheticsMonitorStatus, graphql_name="status")


class SyntheticsScriptBrowserMonitorAdvancedOptions(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("device_emulation", "enable_screenshot_on_failure_and_script")
    device_emulation = sgqlc.types.Field(
        SyntheticsDeviceEmulation, graphql_name="deviceEmulation"
    )

    enable_screenshot_on_failure_and_script = sgqlc.types.Field(
        Boolean, graphql_name="enableScreenshotOnFailureAndScript"
    )


class SyntheticsScriptBrowserMonitorCreateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(SyntheticsMonitorCreateError)),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsScriptBrowserMonitor, graphql_name="monitor")


class SyntheticsScriptBrowserMonitorUpdateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(SyntheticsMonitorUpdateError)),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsScriptBrowserMonitor, graphql_name="monitor")


class SyntheticsSecureCredentialMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("created_at", "description", "errors", "key", "last_update")
    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    description = sgqlc.types.Field(String, graphql_name="description")

    errors = sgqlc.types.Field(
        sgqlc.types.list_of(SyntheticsError), graphql_name="errors"
    )

    key = sgqlc.types.Field(String, graphql_name="key")

    last_update = sgqlc.types.Field(EpochMilliseconds, graphql_name="lastUpdate")


class SyntheticsSimpleBrowserMonitor(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "advanced_options",
        "created_at",
        "guid",
        "id",
        "locations",
        "modified_at",
        "name",
        "period",
        "runtime",
        "status",
        "uri",
    )
    advanced_options = sgqlc.types.Field(
        "SyntheticsSimpleBrowserMonitorAdvancedOptions", graphql_name="advancedOptions"
    )

    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    id = sgqlc.types.Field(ID, graphql_name="id")

    locations = sgqlc.types.Field(SyntheticsLocations, graphql_name="locations")

    modified_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="modifiedAt")

    name = sgqlc.types.Field(String, graphql_name="name")

    period = sgqlc.types.Field(SyntheticsMonitorPeriod, graphql_name="period")

    runtime = sgqlc.types.Field(SyntheticsRuntime, graphql_name="runtime")

    status = sgqlc.types.Field(SyntheticsMonitorStatus, graphql_name="status")

    uri = sgqlc.types.Field(String, graphql_name="uri")


class SyntheticsSimpleBrowserMonitorAdvancedOptions(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "custom_headers",
        "device_emulation",
        "enable_screenshot_on_failure_and_script",
        "response_validation_text",
        "use_tls_validation",
    )
    custom_headers = sgqlc.types.Field(
        sgqlc.types.list_of(SyntheticsCustomHeader), graphql_name="customHeaders"
    )

    device_emulation = sgqlc.types.Field(
        SyntheticsDeviceEmulation, graphql_name="deviceEmulation"
    )

    enable_screenshot_on_failure_and_script = sgqlc.types.Field(
        Boolean, graphql_name="enableScreenshotOnFailureAndScript"
    )

    response_validation_text = sgqlc.types.Field(
        String, graphql_name="responseValidationText"
    )

    use_tls_validation = sgqlc.types.Field(Boolean, graphql_name="useTlsValidation")


class SyntheticsSimpleBrowserMonitorCreateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(SyntheticsMonitorCreateError)),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsSimpleBrowserMonitor, graphql_name="monitor")


class SyntheticsSimpleBrowserMonitorUpdateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(SyntheticsMonitorUpdateError)),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsSimpleBrowserMonitor, graphql_name="monitor")


class SyntheticsSimpleMonitor(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "advanced_options",
        "created_at",
        "guid",
        "id",
        "locations",
        "modified_at",
        "name",
        "period",
        "status",
        "uri",
    )
    advanced_options = sgqlc.types.Field(
        "SyntheticsSimpleMonitorAdvancedOptions", graphql_name="advancedOptions"
    )

    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    id = sgqlc.types.Field(ID, graphql_name="id")

    locations = sgqlc.types.Field(SyntheticsLocations, graphql_name="locations")

    modified_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="modifiedAt")

    name = sgqlc.types.Field(String, graphql_name="name")

    period = sgqlc.types.Field(SyntheticsMonitorPeriod, graphql_name="period")

    status = sgqlc.types.Field(SyntheticsMonitorStatus, graphql_name="status")

    uri = sgqlc.types.Field(String, graphql_name="uri")


class SyntheticsSimpleMonitorAdvancedOptions(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "custom_headers",
        "redirect_is_failure",
        "response_validation_text",
        "should_bypass_head_request",
        "use_tls_validation",
    )
    custom_headers = sgqlc.types.Field(
        sgqlc.types.list_of(SyntheticsCustomHeader), graphql_name="customHeaders"
    )

    redirect_is_failure = sgqlc.types.Field(Boolean, graphql_name="redirectIsFailure")

    response_validation_text = sgqlc.types.Field(
        String, graphql_name="responseValidationText"
    )

    should_bypass_head_request = sgqlc.types.Field(
        Boolean, graphql_name="shouldBypassHeadRequest"
    )

    use_tls_validation = sgqlc.types.Field(Boolean, graphql_name="useTlsValidation")


class SyntheticsSimpleMonitorUpdateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(SyntheticsMonitorUpdateError)),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsSimpleMonitor, graphql_name="monitor")


class SyntheticsStep(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("ordinal", "type", "values")
    ordinal = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="ordinal")

    type = sgqlc.types.Field(
        sgqlc.types.non_null(SyntheticsStepType), graphql_name="type"
    )

    values = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="values"
    )


class SyntheticsStepMonitor(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "advanced_options",
        "created_at",
        "guid",
        "id",
        "locations",
        "modified_at",
        "name",
        "period",
        "status",
        "steps",
    )
    advanced_options = sgqlc.types.Field(
        "SyntheticsStepMonitorAdvancedOptions", graphql_name="advancedOptions"
    )

    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")

    id = sgqlc.types.Field(ID, graphql_name="id")

    locations = sgqlc.types.Field(SyntheticsLocations, graphql_name="locations")

    modified_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="modifiedAt")

    name = sgqlc.types.Field(String, graphql_name="name")

    period = sgqlc.types.Field(SyntheticsMonitorPeriod, graphql_name="period")

    status = sgqlc.types.Field(SyntheticsMonitorStatus, graphql_name="status")

    steps = sgqlc.types.Field(sgqlc.types.list_of(SyntheticsStep), graphql_name="steps")


class SyntheticsStepMonitorAdvancedOptions(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("enable_screenshot_on_failure_and_script",)
    enable_screenshot_on_failure_and_script = sgqlc.types.Field(
        Boolean, graphql_name="enableScreenshotOnFailureAndScript"
    )


class SyntheticsStepMonitorCreateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(SyntheticsMonitorCreateError)),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsStepMonitor, graphql_name="monitor")


class SyntheticsStepMonitorUpdateMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors", "monitor")
    errors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(SyntheticsMonitorUpdateError)),
        graphql_name="errors",
    )

    monitor = sgqlc.types.Field(SyntheticsStepMonitor, graphql_name="monitor")


class SyntheticsSyntheticMonitorAsset(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("type", "url")
    type = sgqlc.types.Field(String, graphql_name="type")

    url = sgqlc.types.Field(String, graphql_name="url")


class TaggingMutationError(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("message", "type")
    message = sgqlc.types.Field(String, graphql_name="message")

    type = sgqlc.types.Field(TaggingMutationErrorType, graphql_name="type")


class TaggingMutationResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("errors",)
    errors = sgqlc.types.Field(
        sgqlc.types.list_of(TaggingMutationError), graphql_name="errors"
    )


class TimeWindow(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("end_time", "start_time")
    end_time = sgqlc.types.Field(EpochMilliseconds, graphql_name="endTime")

    start_time = sgqlc.types.Field(EpochMilliseconds, graphql_name="startTime")


class TimeZoneInfo(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("name", "offset")
    name = sgqlc.types.Field(String, graphql_name="name")

    offset = sgqlc.types.Field(Seconds, graphql_name="offset")


class User(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("email", "id", "name")
    email = sgqlc.types.Field(String, graphql_name="email")

    id = sgqlc.types.Field(Int, graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")


class UserManagementAddUsersToGroupsPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("groups",)
    groups = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("UserManagementGroup")),
        graphql_name="groups",
    )


class UserManagementAuthenticationDomain(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("groups", "id", "name", "provisioning_type", "users")
    groups = sgqlc.types.Field(
        "UserManagementGroups",
        graphql_name="groups",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        UserManagementGroupFilterInput,
                        graphql_name="filter",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `filter` (`UserManagementGroupFilterInput`)
    * `id` (`[ID!]`)
    """

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    provisioning_type = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="provisioningType"
    )

    users = sgqlc.types.Field(
        "UserManagementUsers",
        graphql_name="users",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "filter",
                    sgqlc.types.Arg(
                        UserManagementUserFilterInput,
                        graphql_name="filter",
                        default=None,
                    ),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `filter` (`UserManagementUserFilterInput`)
    * `id` (`[ID!]`)
    """


class UserManagementAuthenticationDomains(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("authentication_domains", "next_cursor", "total_count")
    authentication_domains = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(
                sgqlc.types.non_null(UserManagementAuthenticationDomain)
            )
        ),
        graphql_name="authenticationDomains",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class UserManagementCreateGroupPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("group",)
    group = sgqlc.types.Field("UserManagementGroup", graphql_name="group")


class UserManagementCreateUserPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("created_user",)
    created_user = sgqlc.types.Field(
        "UserManagementCreatedUser", graphql_name="createdUser"
    )


class UserManagementCreatedUser(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("authentication_domain_id", "email", "id", "name", "type")
    authentication_domain_id = sgqlc.types.Field(
        ID, graphql_name="authenticationDomainId"
    )

    email = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="email")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    type = sgqlc.types.Field(
        sgqlc.types.non_null("UserManagementUserType"), graphql_name="type"
    )


class UserManagementDeleteGroupPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("group",)
    group = sgqlc.types.Field("UserManagementGroup", graphql_name="group")


class UserManagementDeleteUserPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("deleted_user",)
    deleted_user = sgqlc.types.Field(
        "UserManagementDeletedUser", graphql_name="deletedUser"
    )


class UserManagementDeletedUser(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class UserManagementGroup(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("display_name", "id", "users")
    display_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="displayName"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    users = sgqlc.types.Field(
        "UserManagementGroupUsers",
        graphql_name="users",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `id` (`[ID!]`)
    """


class UserManagementGroupUser(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("email", "id", "name", "time_zone")
    email = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="email")

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    time_zone = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="timeZone")


class UserManagementGroupUsers(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "total_count", "users")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )

    users = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(UserManagementGroupUser))
        ),
        graphql_name="users",
    )


class UserManagementGroups(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("groups", "next_cursor", "total_count")
    groups = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(UserManagementGroup))
        ),
        graphql_name="groups",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class UserManagementOrganizationStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("authentication_domains", "types")
    authentication_domains = sgqlc.types.Field(
        UserManagementAuthenticationDomains,
        graphql_name="authenticationDomains",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `id` (`[ID!]`)
    """

    types = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("UserManagementOrganizationUserType")),
        graphql_name="types",
    )


class UserManagementOrganizationUserType(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("display_name", "id")
    display_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="displayName"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class UserManagementPendingUpgradeRequest(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("id", "message", "requested_user_type")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    message = sgqlc.types.Field(String, graphql_name="message")

    requested_user_type = sgqlc.types.Field(
        "UserManagementUserType", graphql_name="requestedUserType"
    )


class UserManagementRemoveUsersFromGroupsPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("groups",)
    groups = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(UserManagementGroup)),
        graphql_name="groups",
    )


class UserManagementUpdateGroupPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("group",)
    group = sgqlc.types.Field(UserManagementGroup, graphql_name="group")


class UserManagementUpdateUserPayload(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("user",)
    user = sgqlc.types.Field("UserManagementUser", graphql_name="user")


class UserManagementUser(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "email",
        "email_verification_state",
        "groups",
        "id",
        "last_active",
        "name",
        "pending_upgrade_request",
        "time_zone",
        "type",
    )
    email = sgqlc.types.Field(String, graphql_name="email")

    email_verification_state = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="emailVerificationState"
    )

    groups = sgqlc.types.Field(
        "UserManagementUserGroups",
        graphql_name="groups",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(sgqlc.types.non_null(ID)),
                        graphql_name="id",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `id` (`[ID!]`)
    """

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    last_active = sgqlc.types.Field(DateTime, graphql_name="lastActive")

    name = sgqlc.types.Field(String, graphql_name="name")

    pending_upgrade_request = sgqlc.types.Field(
        UserManagementPendingUpgradeRequest, graphql_name="pendingUpgradeRequest"
    )

    time_zone = sgqlc.types.Field(String, graphql_name="timeZone")

    type = sgqlc.types.Field(
        sgqlc.types.non_null("UserManagementUserType"), graphql_name="type"
    )


class UserManagementUserGroup(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("display_name", "id")
    display_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="displayName"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class UserManagementUserGroups(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("groups", "next_cursor", "total_count")
    groups = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(UserManagementUserGroup))
        ),
        graphql_name="groups",
    )

    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class UserManagementUserType(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("display_name", "id")
    display_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="displayName"
    )

    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class UserManagementUsers(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "total_count", "users")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )

    users = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(UserManagementUser))
        ),
        graphql_name="users",
    )


class UserReference(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("email", "gravatar", "id", "name")
    email = sgqlc.types.Field(String, graphql_name="email")

    gravatar = sgqlc.types.Field(String, graphql_name="gravatar")

    id = sgqlc.types.Field(Int, graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")


class UsersActorStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("user_search",)
    user_search = sgqlc.types.Field(
        "UsersUserSearchResult",
        graphql_name="userSearch",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "query",
                    sgqlc.types.Arg(
                        UsersUserSearchQuery, graphql_name="query", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `query` (`UsersUserSearchQuery`)
    """


class UsersUserSearch(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("email", "name", "user_id")
    email = sgqlc.types.Field(String, graphql_name="email")

    name = sgqlc.types.Field(String, graphql_name="name")

    user_id = sgqlc.types.Field(ID, graphql_name="userId")


class UsersUserSearchResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "total_count", "users")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )

    users = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(UsersUserSearch))
        ),
        graphql_name="users",
    )


class WhatsNewDocsStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("announcement", "news_search")
    announcement = sgqlc.types.Field(
        "WhatsNewAnnouncementContent",
        graphql_name="announcement",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    news_search = sgqlc.types.Field(
        "WhatsNewSearchResult",
        graphql_name="newsSearch",
        args=sgqlc.types.ArgDict(
            (
                (
                    "cursor",
                    sgqlc.types.Arg(String, graphql_name="cursor", default=None),
                ),
                (
                    "query",
                    sgqlc.types.Arg(
                        WhatsNewContentSearchQuery, graphql_name="query", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `cursor` (`String`)
    * `query` (`WhatsNewContentSearchQuery`)
    """


class WhatsNewSearchResult(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("next_cursor", "results", "total_count")
    next_cursor = sgqlc.types.Field(String, graphql_name="nextCursor")

    results = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(WhatsNewContent)),
        graphql_name="results",
    )

    total_count = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="totalCount"
    )


class WorkloadAccountStitchedFields(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ()


class WorkloadAutomaticStatus(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("enabled", "remaining_entities_rule", "rules")
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    remaining_entities_rule = sgqlc.types.Field(
        "WorkloadRemainingEntitiesRule", graphql_name="remainingEntitiesRule"
    )

    rules = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null("WorkloadRegularRule"))
        ),
        graphql_name="rules",
    )


class WorkloadCollection(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account",
        "created_at",
        "created_by",
        "description",
        "entities",
        "entity_search_queries",
        "entity_search_query",
        "guid",
        "id",
        "name",
        "permalink",
        "scope_accounts",
        "status",
        "status_config",
        "updated_at",
        "updated_by",
    )
    account = sgqlc.types.Field(
        sgqlc.types.non_null(AccountReference), graphql_name="account"
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    created_by = sgqlc.types.Field(UserReference, graphql_name="createdBy")

    description = sgqlc.types.Field(String, graphql_name="description")

    entities = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("WorkloadEntityRef")),
        graphql_name="entities",
    )

    entity_search_queries = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("WorkloadEntitySearchQuery")),
        graphql_name="entitySearchQueries",
    )

    entity_search_query = sgqlc.types.Field(String, graphql_name="entitySearchQuery")

    guid = sgqlc.types.Field(sgqlc.types.non_null(EntityGuid), graphql_name="guid")

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    permalink = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="permalink"
    )

    scope_accounts = sgqlc.types.Field(
        sgqlc.types.non_null("WorkloadScopeAccounts"), graphql_name="scopeAccounts"
    )

    status = sgqlc.types.Field(
        sgqlc.types.non_null("WorkloadWorkloadStatus"), graphql_name="status"
    )

    status_config = sgqlc.types.Field(
        "WorkloadStatusConfig", graphql_name="statusConfig"
    )

    updated_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="updatedAt")

    updated_by = sgqlc.types.Field(UserReference, graphql_name="updatedBy")


class WorkloadCollectionWithoutStatus(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "account",
        "created_at",
        "created_by",
        "description",
        "entities",
        "entity_search_queries",
        "entity_search_query",
        "guid",
        "id",
        "name",
        "permalink",
        "scope_accounts",
        "status_config",
        "updated_at",
        "updated_by",
    )
    account = sgqlc.types.Field(
        sgqlc.types.non_null(AccountReference), graphql_name="account"
    )

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    created_by = sgqlc.types.Field(UserReference, graphql_name="createdBy")

    description = sgqlc.types.Field(String, graphql_name="description")

    entities = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("WorkloadEntityRef")),
        graphql_name="entities",
    )

    entity_search_queries = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("WorkloadEntitySearchQuery")),
        graphql_name="entitySearchQueries",
    )

    entity_search_query = sgqlc.types.Field(String, graphql_name="entitySearchQuery")

    guid = sgqlc.types.Field(sgqlc.types.non_null(EntityGuid), graphql_name="guid")

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    permalink = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="permalink"
    )

    scope_accounts = sgqlc.types.Field(
        sgqlc.types.non_null("WorkloadScopeAccounts"), graphql_name="scopeAccounts"
    )

    status_config = sgqlc.types.Field(
        "WorkloadStatusConfig", graphql_name="statusConfig"
    )

    updated_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="updatedAt")

    updated_by = sgqlc.types.Field(UserReference, graphql_name="updatedBy")


class WorkloadEntityRef(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("guid",)
    guid = sgqlc.types.Field(EntityGuid, graphql_name="guid")


class WorkloadEntitySearchQuery(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("created_at", "created_by", "id", "query", "updated_at")
    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(EpochMilliseconds), graphql_name="createdAt"
    )

    created_by = sgqlc.types.Field(UserReference, graphql_name="createdBy")

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    query = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="query")

    updated_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="updatedAt")


class WorkloadRegularRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("entities", "entity_search_queries", "id", "rollup")
    entities = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(WorkloadEntityRef)),
        graphql_name="entities",
    )

    entity_search_queries = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(WorkloadEntitySearchQuery)),
        graphql_name="entitySearchQueries",
    )

    id = sgqlc.types.Field(Int, graphql_name="id")

    rollup = sgqlc.types.Field(
        sgqlc.types.non_null("WorkloadRollup"), graphql_name="rollup"
    )


class WorkloadRemainingEntitiesRule(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("rollup",)
    rollup = sgqlc.types.Field(
        sgqlc.types.non_null("WorkloadRemainingEntitiesRuleRollup"),
        graphql_name="rollup",
    )


class WorkloadRemainingEntitiesRuleRollup(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("group_by", "strategy", "threshold_type", "threshold_value")
    group_by = sgqlc.types.Field(
        sgqlc.types.non_null(WorkloadGroupRemainingEntitiesRuleBy),
        graphql_name="groupBy",
    )

    strategy = sgqlc.types.Field(
        sgqlc.types.non_null(WorkloadRollupStrategy), graphql_name="strategy"
    )

    threshold_type = sgqlc.types.Field(
        WorkloadRuleThresholdType, graphql_name="thresholdType"
    )

    threshold_value = sgqlc.types.Field(Int, graphql_name="thresholdValue")


class WorkloadRollup(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("strategy", "threshold_type", "threshold_value")
    strategy = sgqlc.types.Field(
        sgqlc.types.non_null(WorkloadRollupStrategy), graphql_name="strategy"
    )

    threshold_type = sgqlc.types.Field(
        WorkloadRuleThresholdType, graphql_name="thresholdType"
    )

    threshold_value = sgqlc.types.Field(Int, graphql_name="thresholdValue")


class WorkloadRollupRuleDetails(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = (
        "entity_search_queries",
        "has_individual_entities",
        "not_operational_entities",
        "operational_entities",
        "resulting_group_type",
        "threshold_type",
        "unknown_status_entities",
    )
    entity_search_queries = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)),
        graphql_name="entitySearchQueries",
    )

    has_individual_entities = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="hasIndividualEntities"
    )

    not_operational_entities = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="notOperationalEntities"
    )

    operational_entities = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="operationalEntities"
    )

    resulting_group_type = sgqlc.types.Field(
        sgqlc.types.non_null(WorkloadResultingGroupType),
        graphql_name="resultingGroupType",
    )

    threshold_type = sgqlc.types.Field(
        WorkloadRuleThresholdType, graphql_name="thresholdType"
    )

    unknown_status_entities = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="unknownStatusEntities"
    )


class WorkloadScopeAccounts(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("account_ids",)
    account_ids = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int))),
        graphql_name="accountIds",
    )


class WorkloadStaticStatus(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "enabled", "id", "status", "summary")
    description = sgqlc.types.Field(String, graphql_name="description")

    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="id")

    status = sgqlc.types.Field(
        sgqlc.types.non_null(WorkloadStatusValue), graphql_name="status"
    )

    summary = sgqlc.types.Field(String, graphql_name="summary")


class WorkloadStatus(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "status_source", "status_value", "summary")
    description = sgqlc.types.Field(String, graphql_name="description")

    status_source = sgqlc.types.Field(WorkloadStatusSource, graphql_name="statusSource")

    status_value = sgqlc.types.Field(WorkloadStatusValue, graphql_name="statusValue")

    summary = sgqlc.types.Field(String, graphql_name="summary")


class WorkloadStatusConfig(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("automatic", "static")
    automatic = sgqlc.types.Field(WorkloadAutomaticStatus, graphql_name="automatic")

    static = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(WorkloadStaticStatus)),
        graphql_name="static",
    )


class WorkloadValidAccounts(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("accounts",)
    accounts = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(AccountReference)),
        graphql_name="accounts",
    )


class WorkloadWorkloadStatus(sgqlc.types.Type):
    __schema__ = nerdgraph
    __field_names__ = ("description", "source", "status_details", "summary", "value")
    description = sgqlc.types.Field(String, graphql_name="description")

    source = sgqlc.types.Field(
        sgqlc.types.non_null(WorkloadStatusSource), graphql_name="source"
    )

    status_details = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(WorkloadStatusResult)),
        graphql_name="statusDetails",
    )

    summary = sgqlc.types.Field(String, graphql_name="summary")

    value = sgqlc.types.Field(
        sgqlc.types.non_null(WorkloadStatusValue), graphql_name="value"
    )


class AiIssuesAnomalyIncident(sgqlc.types.Type, AiIssuesIIncident):
    __schema__ = nerdgraph
    __field_names__ = ("anomaly_id",)
    anomaly_id = sgqlc.types.Field(String, graphql_name="anomalyId")


class AiIssuesNewRelicIncident(sgqlc.types.Type, AiIssuesIIncident):
    __schema__ = nerdgraph
    __field_names__ = ("condition_family_id", "policy_ids")
    condition_family_id = sgqlc.types.Field(String, graphql_name="conditionFamilyId")

    policy_ids = sgqlc.types.Field(String, graphql_name="policyIds")


class AiIssuesRestIncident(sgqlc.types.Type, AiIssuesIIncident):
    __schema__ = nerdgraph
    __field_names__ = ("aggregation_tags",)
    aggregation_tags = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(AiIssuesKeyValue)),
        graphql_name="aggregationTags",
    )


class AiWorkflowsCreateResponseError(sgqlc.types.Type, AiWorkflowsResponseError):
    __schema__ = nerdgraph
    __field_names__ = ("type",)
    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsCreateErrorType), graphql_name="type"
    )


class AiWorkflowsDeleteResponseError(sgqlc.types.Type, AiWorkflowsResponseError):
    __schema__ = nerdgraph
    __field_names__ = ("type",)
    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsDeleteErrorType), graphql_name="type"
    )


class AiWorkflowsTestResponseError(sgqlc.types.Type, AiWorkflowsResponseError):
    __schema__ = nerdgraph
    __field_names__ = ("type",)
    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsTestErrorType), graphql_name="type"
    )


class AiWorkflowsUpdateResponseError(sgqlc.types.Type, AiWorkflowsResponseError):
    __schema__ = nerdgraph
    __field_names__ = ("type",)
    type = sgqlc.types.Field(
        sgqlc.types.non_null(AiWorkflowsUpdateErrorType), graphql_name="type"
    )


class AlertsCampfireNotificationChannel(sgqlc.types.Type, AlertsNotificationChannel):
    __schema__ = nerdgraph
    __field_names__ = ()


class AlertsEmailNotificationChannel(sgqlc.types.Type, AlertsNotificationChannel):
    __schema__ = nerdgraph
    __field_names__ = ("config",)
    config = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsEmailNotificationChannelConfig),
        graphql_name="config",
    )


class AlertsHipChatNotificationChannel(sgqlc.types.Type, AlertsNotificationChannel):
    __schema__ = nerdgraph
    __field_names__ = ()


class AlertsNrqlBaselineCondition(sgqlc.types.Type, AlertsNrqlCondition):
    __schema__ = nerdgraph
    __field_names__ = ("baseline_direction",)
    baseline_direction = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsNrqlBaselineDirection),
        graphql_name="baselineDirection",
    )


class AlertsNrqlOutlierCondition(sgqlc.types.Type, AlertsNrqlCondition):
    __schema__ = nerdgraph
    __field_names__ = ("expected_groups", "open_violation_on_group_overlap")
    expected_groups = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name="expectedGroups"
    )

    open_violation_on_group_overlap = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean), graphql_name="openViolationOnGroupOverlap"
    )


class AlertsNrqlStaticCondition(sgqlc.types.Type, AlertsNrqlCondition):
    __schema__ = nerdgraph
    __field_names__ = ()


class AlertsOpsGenieNotificationChannel(sgqlc.types.Type, AlertsNotificationChannel):
    __schema__ = nerdgraph
    __field_names__ = ("config",)
    config = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsOpsGenieNotificationChannelConfig),
        graphql_name="config",
    )


class AlertsPagerDutyNotificationChannel(sgqlc.types.Type, AlertsNotificationChannel):
    __schema__ = nerdgraph
    __field_names__ = ("config",)
    config = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsPagerDutyNotificationChannelConfig),
        graphql_name="config",
    )


class AlertsSlackNotificationChannel(sgqlc.types.Type, AlertsNotificationChannel):
    __schema__ = nerdgraph
    __field_names__ = ("config",)
    config = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsSlackNotificationChannelConfig),
        graphql_name="config",
    )


class AlertsUserNotificationChannel(sgqlc.types.Type, AlertsNotificationChannel):
    __schema__ = nerdgraph
    __field_names__ = ()


class AlertsVictorOpsNotificationChannel(sgqlc.types.Type, AlertsNotificationChannel):
    __schema__ = nerdgraph
    __field_names__ = ("config",)
    config = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsVictorOpsNotificationChannelConfig),
        graphql_name="config",
    )


class AlertsWebhookNotificationChannel(sgqlc.types.Type, AlertsNotificationChannel):
    __schema__ = nerdgraph
    __field_names__ = ("config",)
    config = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsWebhookNotificationChannelConfig),
        graphql_name="config",
    )


class AlertsXMattersNotificationChannel(sgqlc.types.Type, AlertsNotificationChannel):
    __schema__ = nerdgraph
    __field_names__ = ("config",)
    config = sgqlc.types.Field(
        sgqlc.types.non_null(AlertsXMattersNotificationChannelConfig),
        graphql_name="config",
    )


class ApiAccessIngestKey(sgqlc.types.Type, ApiAccessKey):
    __schema__ = nerdgraph
    __field_names__ = ("account", "account_id", "ingest_type")
    account = sgqlc.types.Field(AccountReference, graphql_name="account")

    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    ingest_type = sgqlc.types.Field(ApiAccessIngestKeyType, graphql_name="ingestType")


class ApiAccessIngestKeyError(sgqlc.types.Type, ApiAccessKeyError):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "error_type", "id", "ingest_type")
    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    error_type = sgqlc.types.Field(
        ApiAccessIngestKeyErrorType, graphql_name="errorType"
    )

    id = sgqlc.types.Field(String, graphql_name="id")

    ingest_type = sgqlc.types.Field(ApiAccessIngestKeyType, graphql_name="ingestType")


class ApiAccessUserKey(sgqlc.types.Type, ApiAccessKey):
    __schema__ = nerdgraph
    __field_names__ = ("account", "account_id", "user", "user_id")
    account = sgqlc.types.Field(AccountReference, graphql_name="account")

    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    user = sgqlc.types.Field(UserReference, graphql_name="user")

    user_id = sgqlc.types.Field(Int, graphql_name="userId")


class ApiAccessUserKeyError(sgqlc.types.Type, ApiAccessKeyError):
    __schema__ = nerdgraph
    __field_names__ = ("account_id", "error_type", "id", "user_id")
    account_id = sgqlc.types.Field(Int, graphql_name="accountId")

    error_type = sgqlc.types.Field(ApiAccessUserKeyErrorType, graphql_name="errorType")

    id = sgqlc.types.Field(String, graphql_name="id")

    user_id = sgqlc.types.Field(Int, graphql_name="userId")


class ApmApplicationEntity(
    sgqlc.types.Type, AlertableEntity, ApmBrowserApplicationEntity, Entity
):
    __schema__ = nerdgraph
    __field_names__ = (
        "apm_settings",
        "apm_summary",
        "application_id",
        "application_instances",
        "application_instances_v2",
        "exception",
        "flamegraph",
        "language",
        "metric_grouping_issues",
        "metric_normalization_rule",
        "metric_normalization_rules",
        "running_agent_versions",
        "settings",
    )
    apm_settings = sgqlc.types.Field(
        AgentApplicationSettingsApmBase, graphql_name="apmSettings"
    )

    apm_summary = sgqlc.types.Field(
        ApmApplicationSummaryData, graphql_name="apmSummary"
    )

    application_id = sgqlc.types.Field(Int, graphql_name="applicationId")

    application_instances = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(AgentEnvironmentApplicationInstance)),
        graphql_name="applicationInstances",
        args=sgqlc.types.ArgDict(
            (
                (
                    "end_time",
                    sgqlc.types.Arg(
                        EpochMilliseconds, graphql_name="endTime", default=None
                    ),
                ),
                ("host", sgqlc.types.Arg(String, graphql_name="host", default=None)),
                (
                    "start_time",
                    sgqlc.types.Arg(
                        EpochMilliseconds, graphql_name="startTime", default=None
                    ),
                ),
            )
        ),
    )

    application_instances_v2 = sgqlc.types.Field(
        sgqlc.types.non_null(AgentEnvironmentApplicationInstancesResult),
        graphql_name="applicationInstancesV2",
        args=sgqlc.types.ArgDict(
            (("cursor", sgqlc.types.Arg(String, graphql_name="cursor", default=None)),)
        ),
    )

    exception = sgqlc.types.Field(
        StackTraceApmException,
        graphql_name="exception",
        args=sgqlc.types.ArgDict(
            (
                (
                    "occurrence_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="occurrenceId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    flamegraph = sgqlc.types.Field(
        JavaFlightRecorderFlamegraph,
        graphql_name="flamegraph",
        args=sgqlc.types.ArgDict(
            (
                (
                    "host_name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="hostName",
                        default=None,
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )

    language = sgqlc.types.Field(String, graphql_name="language")

    metric_grouping_issues = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(MetricNormalizationRuleMetricGroupingIssue)
        ),
        graphql_name="metricGroupingIssues",
        args=sgqlc.types.ArgDict(
            (
                (
                    "end_time",
                    sgqlc.types.Arg(
                        EpochMilliseconds, graphql_name="endTime", default=None
                    ),
                ),
                (
                    "metric_normalization_rule_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(Int),
                        graphql_name="metricNormalizationRuleIds",
                        default=None,
                    ),
                ),
                (
                    "start_time",
                    sgqlc.types.Arg(
                        EpochMilliseconds, graphql_name="startTime", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `end_time` (`EpochMilliseconds`)
    * `metric_normalization_rule_ids` (`[Int]`)
    * `start_time` (`EpochMilliseconds`)
    """

    metric_normalization_rule = sgqlc.types.Field(
        MetricNormalizationRule,
        graphql_name="metricNormalizationRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    metric_normalization_rules = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(MetricNormalizationRule)),
        graphql_name="metricNormalizationRules",
        args=sgqlc.types.ArgDict(
            (
                (
                    "enabled",
                    sgqlc.types.Arg(Boolean, graphql_name="enabled", default=None),
                ),
            )
        ),
    )

    running_agent_versions = sgqlc.types.Field(
        ApmApplicationRunningAgentVersions, graphql_name="runningAgentVersions"
    )

    settings = sgqlc.types.Field(ApmApplicationSettings, graphql_name="settings")


class ApmApplicationEntityOutline(
    sgqlc.types.Type,
    AlertableEntityOutline,
    ApmBrowserApplicationEntityOutline,
    EntityOutline,
):
    __schema__ = nerdgraph
    __field_names__ = (
        "apm_summary",
        "application_id",
        "language",
        "running_agent_versions",
        "settings",
    )
    apm_summary = sgqlc.types.Field(
        ApmApplicationSummaryData, graphql_name="apmSummary"
    )

    application_id = sgqlc.types.Field(Int, graphql_name="applicationId")

    language = sgqlc.types.Field(String, graphql_name="language")

    running_agent_versions = sgqlc.types.Field(
        ApmApplicationRunningAgentVersions, graphql_name="runningAgentVersions"
    )

    settings = sgqlc.types.Field(ApmApplicationSettings, graphql_name="settings")


class ApmDatabaseInstanceEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = ("host", "port_or_path", "vendor")
    host = sgqlc.types.Field(String, graphql_name="host")

    port_or_path = sgqlc.types.Field(String, graphql_name="portOrPath")

    vendor = sgqlc.types.Field(String, graphql_name="vendor")


class ApmDatabaseInstanceEntityOutline(
    sgqlc.types.Type, AlertableEntityOutline, EntityOutline
):
    __schema__ = nerdgraph
    __field_names__ = ("host", "port_or_path", "vendor")
    host = sgqlc.types.Field(String, graphql_name="host")

    port_or_path = sgqlc.types.Field(String, graphql_name="portOrPath")

    vendor = sgqlc.types.Field(String, graphql_name="vendor")


class ApmExternalServiceEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = ("host",)
    host = sgqlc.types.Field(String, graphql_name="host")


class ApmExternalServiceEntityOutline(
    sgqlc.types.Type, AlertableEntityOutline, EntityOutline
):
    __schema__ = nerdgraph
    __field_names__ = ("host",)
    host = sgqlc.types.Field(String, graphql_name="host")


class BrowserApplicationEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = (
        "agent_install_type",
        "application_id",
        "browser_properties",
        "browser_settings",
        "browser_summary",
        "exception",
        "metric_grouping_issues",
        "metric_normalization_rule",
        "metric_normalization_rules",
        "running_agent_versions",
        "serving_apm_application_id",
        "settings",
    )
    agent_install_type = sgqlc.types.Field(
        BrowserAgentInstallType, graphql_name="agentInstallType"
    )

    application_id = sgqlc.types.Field(Int, graphql_name="applicationId")

    browser_properties = sgqlc.types.Field(
        AgentApplicationSettingsBrowserProperties, graphql_name="browserProperties"
    )

    browser_settings = sgqlc.types.Field(
        AgentApplicationSettingsBrowserBase, graphql_name="browserSettings"
    )

    browser_summary = sgqlc.types.Field(
        BrowserApplicationSummaryData, graphql_name="browserSummary"
    )

    exception = sgqlc.types.Field(
        StackTraceBrowserException,
        graphql_name="exception",
        args=sgqlc.types.ArgDict(
            (
                (
                    "fingerprint",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="fingerprint",
                        default=None,
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )

    metric_grouping_issues = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(MetricNormalizationRuleMetricGroupingIssue)
        ),
        graphql_name="metricGroupingIssues",
        args=sgqlc.types.ArgDict(
            (
                (
                    "end_time",
                    sgqlc.types.Arg(
                        EpochMilliseconds, graphql_name="endTime", default=None
                    ),
                ),
                (
                    "metric_normalization_rule_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(Int),
                        graphql_name="metricNormalizationRuleIds",
                        default=None,
                    ),
                ),
                (
                    "start_time",
                    sgqlc.types.Arg(
                        EpochMilliseconds, graphql_name="startTime", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `end_time` (`EpochMilliseconds`)
    * `metric_normalization_rule_ids` (`[Int]`)
    * `start_time` (`EpochMilliseconds`)
    """

    metric_normalization_rule = sgqlc.types.Field(
        MetricNormalizationRule,
        graphql_name="metricNormalizationRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    metric_normalization_rules = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(MetricNormalizationRule)),
        graphql_name="metricNormalizationRules",
        args=sgqlc.types.ArgDict(
            (
                (
                    "enabled",
                    sgqlc.types.Arg(Boolean, graphql_name="enabled", default=None),
                ),
            )
        ),
    )

    running_agent_versions = sgqlc.types.Field(
        BrowserApplicationRunningAgentVersions, graphql_name="runningAgentVersions"
    )

    serving_apm_application_id = sgqlc.types.Field(
        Int, graphql_name="servingApmApplicationId"
    )

    settings = sgqlc.types.Field(BrowserApplicationSettings, graphql_name="settings")


class BrowserApplicationEntityOutline(
    sgqlc.types.Type, AlertableEntityOutline, EntityOutline
):
    __schema__ = nerdgraph
    __field_names__ = (
        "agent_install_type",
        "application_id",
        "browser_summary",
        "running_agent_versions",
        "serving_apm_application_id",
        "settings",
    )
    agent_install_type = sgqlc.types.Field(
        BrowserAgentInstallType, graphql_name="agentInstallType"
    )

    application_id = sgqlc.types.Field(Int, graphql_name="applicationId")

    browser_summary = sgqlc.types.Field(
        BrowserApplicationSummaryData, graphql_name="browserSummary"
    )

    running_agent_versions = sgqlc.types.Field(
        BrowserApplicationRunningAgentVersions, graphql_name="runningAgentVersions"
    )

    serving_apm_application_id = sgqlc.types.Field(
        Int, graphql_name="servingApmApplicationId"
    )

    settings = sgqlc.types.Field(BrowserApplicationSettings, graphql_name="settings")


class CloudAlbIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_extended_inventory",
        "fetch_tags",
        "load_balancer_prefixes",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_extended_inventory = sgqlc.types.Field(
        Boolean, graphql_name="fetchExtendedInventory"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    load_balancer_prefixes = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="loadBalancerPrefixes"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudApigatewayIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "metrics_polling_interval",
        "stage_prefixes",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    stage_prefixes = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="stagePrefixes"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudAutoscalingIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsAppsyncIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsAthenaIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsCognitoIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsConnectIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsDirectconnectIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsDocdbIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsFsxIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsGlueIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsGovCloudProvider(sgqlc.types.Type, CloudProvider):
    __schema__ = nerdgraph
    __field_names__ = ("aws_account_id",)
    aws_account_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="awsAccountId"
    )


class CloudAwsKinesisanalyticsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsMediaconvertIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsMediapackagevodIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsMetadataIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsMqIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsMskIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsNeptuneIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsProvider(sgqlc.types.Type, CloudProvider):
    __schema__ = nerdgraph
    __field_names__ = ("role_account_id", "role_external_id")
    role_account_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="roleAccountId"
    )

    role_external_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="roleExternalId"
    )


class CloudAwsQldbIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsRoute53resolverIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsStatesIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsTagsGlobalIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsTransitgatewayIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsWafIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsWafv2Integration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAwsXrayIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudAzureApimanagementIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureAppgatewayIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureAppserviceIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureContainersIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureCosmosdbIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureCostmanagementIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "tag_keys")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_keys = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name="tagKeys")


class CloudAzureDatafactoryIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureEventhubIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureExpressrouteIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureFirewallsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureFrontdoorIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureFunctionsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureKeyvaultIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureLoadbalancerIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureLogicappsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureMachinelearningIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureMariadbIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureMonitorIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "enabled",
        "exclude_tags",
        "include_tags",
        "inventory_polling_interval",
        "metrics_polling_interval",
        "resource_groups",
        "resource_types",
    )
    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")

    exclude_tags = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="excludeTags"
    )

    include_tags = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="includeTags"
    )

    inventory_polling_interval = sgqlc.types.Field(
        Int, graphql_name="inventoryPollingInterval"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )

    resource_types = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceTypes"
    )


class CloudAzureMysqlIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureMysqlflexibleIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzurePostgresqlIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzurePostgresqlflexibleIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzurePowerbidedicatedIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureRediscacheIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureServicebusIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureSqlIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureSqlmanagedIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureStorageIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureVirtualmachineIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureVirtualnetworksIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureVmsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudAzureVpngatewaysIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "resource_groups")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    resource_groups = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="resourceGroups"
    )


class CloudBaseIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ()


class CloudBaseProvider(sgqlc.types.Type, CloudProvider):
    __schema__ = nerdgraph
    __field_names__ = ()


class CloudBillingIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudCloudfrontIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "fetch_lambdas_at_edge",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    fetch_lambdas_at_edge = sgqlc.types.Field(
        Boolean, graphql_name="fetchLambdasAtEdge"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudCloudtrailIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudDynamodbIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_extended_inventory",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_extended_inventory = sgqlc.types.Field(
        Boolean, graphql_name="fetchExtendedInventory"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudEbsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_extended_inventory",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_extended_inventory = sgqlc.types.Field(
        Boolean, graphql_name="fetchExtendedInventory"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudEc2Integration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "duplicate_ec2_tags",
        "fetch_ip_addresses",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    duplicate_ec2_tags = sgqlc.types.Field(Boolean, graphql_name="duplicateEc2Tags")

    fetch_ip_addresses = sgqlc.types.Field(Boolean, graphql_name="fetchIpAddresses")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudEcsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudEfsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudElasticacheIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudElasticbeanstalkIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_extended_inventory",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_extended_inventory = sgqlc.types.Field(
        Boolean, graphql_name="fetchExtendedInventory"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudElasticsearchIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_nodes",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_nodes = sgqlc.types.Field(Boolean, graphql_name="fetchNodes")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudElbIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_extended_inventory",
        "fetch_tags",
        "metrics_polling_interval",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_extended_inventory = sgqlc.types.Field(
        Boolean, graphql_name="fetchExtendedInventory"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudEmrIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudGcpAlloydbIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpAppengineIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpBigqueryIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("fetch_table_metrics", "fetch_tags", "metrics_polling_interval")
    fetch_table_metrics = sgqlc.types.Field(Boolean, graphql_name="fetchTableMetrics")

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpBigtableIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpComposerIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpDataflowIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpDataprocIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpDatastoreIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpFirebasedatabaseIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpFirebasehostingIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpFirebasestorageIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpFirestoreIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpFunctionsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpInterconnectIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpKubernetesIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpLoadbalancingIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpMemcacheIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpProvider(sgqlc.types.Type, CloudProvider):
    __schema__ = nerdgraph
    __field_names__ = ("service_account_id",)
    service_account_id = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="serviceAccountId"
    )


class CloudGcpPubsubIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("fetch_tags", "metrics_polling_interval")
    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpRedisIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpRouterIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpRunIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpSpannerIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("fetch_tags", "metrics_polling_interval")
    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpSqlIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpStorageIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("fetch_tags", "metrics_polling_interval")
    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpVmsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudGcpVpcaccessIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudHealthIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudIamIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval", "tag_key", "tag_value")
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudIotIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudKinesisFirehoseIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudKinesisIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_shards",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_shards = sgqlc.types.Field(Boolean, graphql_name="fetchShards")

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudLambdaIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudRdsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudRedshiftIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudRoute53Integration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("fetch_extended_inventory", "metrics_polling_interval")
    fetch_extended_inventory = sgqlc.types.Field(
        Boolean, graphql_name="fetchExtendedInventory"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudS3Integration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "fetch_extended_inventory",
        "fetch_tags",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    fetch_extended_inventory = sgqlc.types.Field(
        Boolean, graphql_name="fetchExtendedInventory"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudSesIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("aws_regions", "metrics_polling_interval")
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudSnsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_extended_inventory",
        "metrics_polling_interval",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_extended_inventory = sgqlc.types.Field(
        Boolean, graphql_name="fetchExtendedInventory"
    )

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudSqsIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_extended_inventory",
        "fetch_tags",
        "metrics_polling_interval",
        "queue_prefixes",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_extended_inventory = sgqlc.types.Field(
        Boolean, graphql_name="fetchExtendedInventory"
    )

    fetch_tags = sgqlc.types.Field(Boolean, graphql_name="fetchTags")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    queue_prefixes = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="queuePrefixes"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class CloudTrustedadvisorIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = ("metrics_polling_interval",)
    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )


class CloudVpcIntegration(sgqlc.types.Type, CloudIntegration):
    __schema__ = nerdgraph
    __field_names__ = (
        "aws_regions",
        "fetch_nat_gateway",
        "fetch_vpn",
        "metrics_polling_interval",
        "tag_key",
        "tag_value",
    )
    aws_regions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name="awsRegions"
    )

    fetch_nat_gateway = sgqlc.types.Field(Boolean, graphql_name="fetchNatGateway")

    fetch_vpn = sgqlc.types.Field(Boolean, graphql_name="fetchVpn")

    metrics_polling_interval = sgqlc.types.Field(
        Int, graphql_name="metricsPollingInterval"
    )

    tag_key = sgqlc.types.Field(String, graphql_name="tagKey")

    tag_value = sgqlc.types.Field(String, graphql_name="tagValue")


class DashboardEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "dashboard_parent_guid",
        "description",
        "owner",
        "pages",
        "permissions",
        "updated_at",
        "variables",
    )
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")

    dashboard_parent_guid = sgqlc.types.Field(
        EntityGuid, graphql_name="dashboardParentGuid"
    )

    description = sgqlc.types.Field(String, graphql_name="description")

    owner = sgqlc.types.Field(DashboardEntityOwnerInfo, graphql_name="owner")

    pages = sgqlc.types.Field(sgqlc.types.list_of(DashboardPage), graphql_name="pages")

    permissions = sgqlc.types.Field(
        DashboardEntityPermissions, graphql_name="permissions"
    )

    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")

    variables = sgqlc.types.Field(
        sgqlc.types.list_of(DashboardVariable), graphql_name="variables"
    )


class DashboardEntityOutline(sgqlc.types.Type, AlertableEntityOutline, EntityOutline):
    __schema__ = nerdgraph
    __field_names__ = (
        "created_at",
        "dashboard_parent_guid",
        "owner",
        "permissions",
        "updated_at",
    )
    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")

    dashboard_parent_guid = sgqlc.types.Field(
        EntityGuid, graphql_name="dashboardParentGuid"
    )

    owner = sgqlc.types.Field(DashboardEntityOwnerInfo, graphql_name="owner")

    permissions = sgqlc.types.Field(
        DashboardEntityPermissions, graphql_name="permissions"
    )

    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class EdgeAgentEndpointDetail(sgqlc.types.Type, EdgeEndpointDetail):
    __schema__ = nerdgraph
    __field_names__ = ()


class EdgeHttpsEndpointDetail(sgqlc.types.Type, EdgeEndpointDetail):
    __schema__ = nerdgraph
    __field_names__ = ("url",)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class EntityRelationshipDetectedEdge(sgqlc.types.Type, EntityRelationshipEdge):
    __schema__ = nerdgraph
    __field_names__ = ()


class EntityRelationshipUserDefinedEdge(sgqlc.types.Type, EntityRelationshipEdge):
    __schema__ = nerdgraph
    __field_names__ = ("created_by_user",)
    created_by_user = sgqlc.types.Field(UserReference, graphql_name="createdByUser")


class ErrorsInboxAssignErrorGroupError(sgqlc.types.Type, ErrorsInboxResponseError):
    __schema__ = nerdgraph
    __field_names__ = ("type",)
    type = sgqlc.types.Field(
        sgqlc.types.non_null(ErrorsInboxAssignErrorGroupErrorType), graphql_name="type"
    )


class ErrorsInboxJiraIssue(sgqlc.types.Type, ErrorsInboxResource):
    __schema__ = nerdgraph
    __field_names__ = ("issue_id",)
    issue_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="issueId")


class ErrorsInboxUpdateErrorGroupStateError(sgqlc.types.Type, ErrorsInboxResponseError):
    __schema__ = nerdgraph
    __field_names__ = ("type",)
    type = sgqlc.types.Field(
        sgqlc.types.non_null(ErrorsInboxUpdateErrorGroupStateErrorType),
        graphql_name="type",
    )


class ExternalEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = ()


class ExternalEntityOutline(sgqlc.types.Type, AlertableEntityOutline, EntityOutline):
    __schema__ = nerdgraph
    __field_names__ = ()


class GenericEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = ()


class GenericEntityOutline(sgqlc.types.Type, AlertableEntityOutline, EntityOutline):
    __schema__ = nerdgraph
    __field_names__ = ()


class GenericInfrastructureEntity(
    sgqlc.types.Type, AlertableEntity, Entity, InfrastructureIntegrationEntity
):
    __schema__ = nerdgraph
    __field_names__ = ()


class GenericInfrastructureEntityOutline(
    sgqlc.types.Type,
    AlertableEntityOutline,
    EntityOutline,
    InfrastructureIntegrationEntityOutline,
):
    __schema__ = nerdgraph
    __field_names__ = ()


class InfrastructureAwsLambdaFunctionEntity(
    sgqlc.types.Type, AlertableEntity, Entity, InfrastructureIntegrationEntity
):
    __schema__ = nerdgraph
    __field_names__ = ("runtime",)
    runtime = sgqlc.types.Field(String, graphql_name="runtime")


class InfrastructureAwsLambdaFunctionEntityOutline(
    sgqlc.types.Type,
    AlertableEntityOutline,
    EntityOutline,
    InfrastructureIntegrationEntityOutline,
):
    __schema__ = nerdgraph
    __field_names__ = ("runtime",)
    runtime = sgqlc.types.Field(String, graphql_name="runtime")


class InfrastructureHostEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = ("host_summary",)
    host_summary = sgqlc.types.Field(
        InfrastructureHostSummaryData, graphql_name="hostSummary"
    )


class InfrastructureHostEntityOutline(
    sgqlc.types.Type, AlertableEntityOutline, EntityOutline
):
    __schema__ = nerdgraph
    __field_names__ = ("host_summary",)
    host_summary = sgqlc.types.Field(
        InfrastructureHostSummaryData, graphql_name="hostSummary"
    )


class KeyTransactionEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = (
        "apdex_target",
        "application",
        "browser_apdex_target",
        "metric_name",
    )
    apdex_target = sgqlc.types.Field(
        sgqlc.types.non_null(Float), graphql_name="apdexTarget"
    )

    application = sgqlc.types.Field(
        sgqlc.types.non_null(KeyTransactionApplication), graphql_name="application"
    )

    browser_apdex_target = sgqlc.types.Field(Float, graphql_name="browserApdexTarget")

    metric_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="metricName"
    )


class KeyTransactionEntityOutline(
    sgqlc.types.Type, AlertableEntityOutline, EntityOutline
):
    __schema__ = nerdgraph
    __field_names__ = ()


class MobileApplicationEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = (
        "application_id",
        "crash",
        "exception",
        "metric_grouping_issues",
        "metric_normalization_rule",
        "metric_normalization_rules",
        "mobile_properties",
        "mobile_settings",
        "mobile_summary",
    )
    application_id = sgqlc.types.Field(Int, graphql_name="applicationId")

    crash = sgqlc.types.Field(
        StackTraceMobileCrash,
        graphql_name="crash",
        args=sgqlc.types.ArgDict(
            (
                (
                    "occurrence_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="occurrenceId",
                        default=None,
                    ),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )

    exception = sgqlc.types.Field(
        StackTraceMobileException,
        graphql_name="exception",
        args=sgqlc.types.ArgDict(
            (
                (
                    "fingerprint",
                    sgqlc.types.Arg(String, graphql_name="fingerprint", default=None),
                ),
                (
                    "occurrence_id",
                    sgqlc.types.Arg(String, graphql_name="occurrenceId", default=None),
                ),
                (
                    "time_window",
                    sgqlc.types.Arg(
                        TimeWindowInput, graphql_name="timeWindow", default=None
                    ),
                ),
            )
        ),
    )

    metric_grouping_issues = sgqlc.types.Field(
        sgqlc.types.list_of(
            sgqlc.types.non_null(MetricNormalizationRuleMetricGroupingIssue)
        ),
        graphql_name="metricGroupingIssues",
        args=sgqlc.types.ArgDict(
            (
                (
                    "end_time",
                    sgqlc.types.Arg(
                        EpochMilliseconds, graphql_name="endTime", default=None
                    ),
                ),
                (
                    "metric_normalization_rule_ids",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(Int),
                        graphql_name="metricNormalizationRuleIds",
                        default=None,
                    ),
                ),
                (
                    "start_time",
                    sgqlc.types.Arg(
                        EpochMilliseconds, graphql_name="startTime", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `end_time` (`EpochMilliseconds`)
    * `metric_normalization_rule_ids` (`[Int]`)
    * `start_time` (`EpochMilliseconds`)
    """

    metric_normalization_rule = sgqlc.types.Field(
        MetricNormalizationRule,
        graphql_name="metricNormalizationRule",
        args=sgqlc.types.ArgDict(
            (
                (
                    "id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name="id", default=None
                    ),
                ),
            )
        ),
    )

    metric_normalization_rules = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(MetricNormalizationRule)),
        graphql_name="metricNormalizationRules",
        args=sgqlc.types.ArgDict(
            (
                (
                    "enabled",
                    sgqlc.types.Arg(Boolean, graphql_name="enabled", default=None),
                ),
            )
        ),
    )

    mobile_properties = sgqlc.types.Field(
        AgentApplicationSettingsMobileProperties, graphql_name="mobileProperties"
    )

    mobile_settings = sgqlc.types.Field(
        AgentApplicationSettingsMobileBase, graphql_name="mobileSettings"
    )

    mobile_summary = sgqlc.types.Field(
        MobileAppSummaryData, graphql_name="mobileSummary"
    )


class MobileApplicationEntityOutline(
    sgqlc.types.Type, AlertableEntityOutline, EntityOutline
):
    __schema__ = nerdgraph
    __field_names__ = ("application_id", "mobile_summary")
    application_id = sgqlc.types.Field(Int, graphql_name="applicationId")

    mobile_summary = sgqlc.types.Field(
        MobileAppSummaryData, graphql_name="mobileSummary"
    )


class Nr1CatalogAllSupportedEntityTypes(
    sgqlc.types.Type, Nr1CatalogSupportedEntityTypes
):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogInstallPlan(sgqlc.types.Type, Nr1CatalogInstaller):
    __schema__ = nerdgraph
    __field_names__ = ("steps",)
    steps = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogInstallPlanStep))
        ),
        graphql_name="steps",
    )


class Nr1CatalogLauncher(sgqlc.types.Type, Nr1CatalogNerdpackItem):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogLauncherMetadata(sgqlc.types.Type, Nr1CatalogNerdpackItemMetadata):
    __schema__ = nerdgraph
    __field_names__ = ("icon",)
    icon = sgqlc.types.Field(Nr1CatalogIcon, graphql_name="icon")


class Nr1CatalogLinkInstallPlanDirective(
    sgqlc.types.Type, Nr1CatalogInstallPlanDirective
):
    __schema__ = nerdgraph
    __field_names__ = ("url",)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class Nr1CatalogNerdlet(sgqlc.types.Type, Nr1CatalogNerdpackItem):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogNerdletInstallPlanDirective(
    sgqlc.types.Type, Nr1CatalogInstallPlanDirective
):
    __schema__ = nerdgraph
    __field_names__ = ("nerdlet_id", "nerdlet_state")
    nerdlet_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="nerdletId")

    nerdlet_state = sgqlc.types.Field(
        Nr1CatalogRawNerdletState, graphql_name="nerdletState"
    )


class Nr1CatalogNerdletMetadata(sgqlc.types.Type, Nr1CatalogNerdpackItemMetadata):
    __schema__ = nerdgraph
    __field_names__ = ("supported_entity_types",)
    supported_entity_types = sgqlc.types.Field(
        Nr1CatalogSupportedEntityTypes, graphql_name="supportedEntityTypes"
    )


class Nr1CatalogNoSupportedEntityTypes(
    sgqlc.types.Type, Nr1CatalogSupportedEntityTypes
):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogQuickstartAlert(sgqlc.types.Type, Nr1CatalogQuickstartComponent):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogQuickstartAlertCondition(
    sgqlc.types.Type, Nr1CatalogQuickstartComponent
):
    __schema__ = nerdgraph
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class Nr1CatalogQuickstartAlertConditionMetadata(
    sgqlc.types.Type, Nr1CatalogQuickstartComponentMetadata
):
    __schema__ = nerdgraph
    __field_names__ = ("type",)
    type = sgqlc.types.Field(
        sgqlc.types.non_null(Nr1CatalogQuickstartAlertConditionType),
        graphql_name="type",
    )


class Nr1CatalogQuickstartAlertMetadata(
    sgqlc.types.Type, Nr1CatalogQuickstartComponentMetadata
):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogQuickstartDashboard(sgqlc.types.Type, Nr1CatalogQuickstartComponent):
    __schema__ = nerdgraph
    __field_names__ = ("id",)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")


class Nr1CatalogQuickstartDashboardMetadata(
    sgqlc.types.Type, Nr1CatalogQuickstartComponentMetadata
):
    __schema__ = nerdgraph
    __field_names__ = ("previews",)
    previews = sgqlc.types.Field(
        sgqlc.types.non_null(
            sgqlc.types.list_of(sgqlc.types.non_null(Nr1CatalogPreview))
        ),
        graphql_name="previews",
    )


class Nr1CatalogQuickstartDocumentation(
    sgqlc.types.Type, Nr1CatalogQuickstartComponent
):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogQuickstartDocumentationMetadata(
    sgqlc.types.Type, Nr1CatalogQuickstartComponentMetadata
):
    __schema__ = nerdgraph
    __field_names__ = ("url",)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="url")


class Nr1CatalogQuickstartInstallPlan(sgqlc.types.Type, Nr1CatalogQuickstartComponent):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogQuickstartInstallPlanMetadata(
    sgqlc.types.Type, Nr1CatalogQuickstartComponentMetadata
):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogScreenshot(sgqlc.types.Type, Nr1CatalogPreview):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogSpecificSupportedEntityTypes(
    sgqlc.types.Type, Nr1CatalogSupportedEntityTypes
):
    __schema__ = nerdgraph
    __field_names__ = ("entity_types",)
    entity_types = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DomainType))),
        graphql_name="entityTypes",
    )


class Nr1CatalogTargetedInstallPlanDirective(
    sgqlc.types.Type, Nr1CatalogInstallPlanDirective
):
    __schema__ = nerdgraph
    __field_names__ = ("recipe_name",)
    recipe_name = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name="recipeName"
    )


class Nr1CatalogVisualization(sgqlc.types.Type, Nr1CatalogNerdpackItem):
    __schema__ = nerdgraph
    __field_names__ = ()


class Nr1CatalogVisualizationMetadata(sgqlc.types.Type, Nr1CatalogNerdpackItemMetadata):
    __schema__ = nerdgraph
    __field_names__ = ()


class SecureCredentialEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = (
        "description",
        "secure_credential_id",
        "secure_credential_summary",
        "updated_at",
    )
    description = sgqlc.types.Field(String, graphql_name="description")

    secure_credential_id = sgqlc.types.Field(ID, graphql_name="secureCredentialId")

    secure_credential_summary = sgqlc.types.Field(
        SecureCredentialSummaryData, graphql_name="secureCredentialSummary"
    )

    updated_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="updatedAt")


class SecureCredentialEntityOutline(
    sgqlc.types.Type, AlertableEntityOutline, EntityOutline
):
    __schema__ = nerdgraph
    __field_names__ = (
        "description",
        "secure_credential_id",
        "secure_credential_summary",
        "updated_at",
    )
    description = sgqlc.types.Field(String, graphql_name="description")

    secure_credential_id = sgqlc.types.Field(ID, graphql_name="secureCredentialId")

    secure_credential_summary = sgqlc.types.Field(
        SecureCredentialSummaryData, graphql_name="secureCredentialSummary"
    )

    updated_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="updatedAt")


class SuggestedAnomalyBasedNrqlQuery(sgqlc.types.Type, SuggestedNrqlQuery):
    __schema__ = nerdgraph
    __field_names__ = ("anomaly",)
    anomaly = sgqlc.types.Field(
        sgqlc.types.non_null(SuggestedNrqlQueryAnomaly), graphql_name="anomaly"
    )


class SuggestedHistoryBasedNrqlQuery(sgqlc.types.Type, SuggestedNrqlQuery):
    __schema__ = nerdgraph
    __field_names__ = ()


class SyntheticMonitorEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = (
        "assets",
        "monitor_id",
        "monitor_summary",
        "monitor_type",
        "monitored_url",
        "period",
    )
    assets = sgqlc.types.Field(
        sgqlc.types.list_of(SyntheticsSyntheticMonitorAsset),
        graphql_name="assets",
        args=sgqlc.types.ArgDict(
            (
                (
                    "check_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="checkId",
                        default=None,
                    ),
                ),
            )
        ),
    )

    monitor_id = sgqlc.types.Field(ID, graphql_name="monitorId")

    monitor_summary = sgqlc.types.Field(
        SyntheticMonitorSummaryData, graphql_name="monitorSummary"
    )

    monitor_type = sgqlc.types.Field(SyntheticMonitorType, graphql_name="monitorType")

    monitored_url = sgqlc.types.Field(String, graphql_name="monitoredUrl")

    period = sgqlc.types.Field(Minutes, graphql_name="period")


class SyntheticMonitorEntityOutline(
    sgqlc.types.Type, AlertableEntityOutline, EntityOutline
):
    __schema__ = nerdgraph
    __field_names__ = (
        "monitor_id",
        "monitor_summary",
        "monitor_type",
        "monitored_url",
        "period",
    )
    monitor_id = sgqlc.types.Field(ID, graphql_name="monitorId")

    monitor_summary = sgqlc.types.Field(
        SyntheticMonitorSummaryData, graphql_name="monitorSummary"
    )

    monitor_type = sgqlc.types.Field(SyntheticMonitorType, graphql_name="monitorType")

    monitored_url = sgqlc.types.Field(String, graphql_name="monitoredUrl")

    period = sgqlc.types.Field(Minutes, graphql_name="period")


class TeamEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = ()


class TeamEntityOutline(sgqlc.types.Type, AlertableEntityOutline, EntityOutline):
    __schema__ = nerdgraph
    __field_names__ = ()


class ThirdPartyServiceEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = ()


class ThirdPartyServiceEntityOutline(
    sgqlc.types.Type, AlertableEntityOutline, EntityOutline
):
    __schema__ = nerdgraph
    __field_names__ = ()


class UnavailableEntity(sgqlc.types.Type, AlertableEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = ()


class UnavailableEntityOutline(sgqlc.types.Type, AlertableEntityOutline, EntityOutline):
    __schema__ = nerdgraph
    __field_names__ = ()


class WhatsNewAnnouncementContent(sgqlc.types.Type, WhatsNewContent):
    __schema__ = nerdgraph
    __field_names__ = (
        "body",
        "doc_url",
        "getting_started_url",
        "is_featured",
        "learn_more_url",
        "requirements",
    )
    body = sgqlc.types.Field(String, graphql_name="body")

    doc_url = sgqlc.types.Field(String, graphql_name="docUrl")

    getting_started_url = sgqlc.types.Field(String, graphql_name="gettingStartedUrl")

    is_featured = sgqlc.types.Field(Boolean, graphql_name="isFeatured")

    learn_more_url = sgqlc.types.Field(String, graphql_name="learnMoreUrl")

    requirements = sgqlc.types.Field(String, graphql_name="requirements")


class WorkloadEntity(sgqlc.types.Type, AlertableEntity, CollectionEntity, Entity):
    __schema__ = nerdgraph
    __field_names__ = ("created_at", "created_by_user", "updated_at", "workload_status")
    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    created_by_user = sgqlc.types.Field(UserReference, graphql_name="createdByUser")

    updated_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="updatedAt")

    workload_status = sgqlc.types.Field(WorkloadStatus, graphql_name="workloadStatus")


class WorkloadEntityOutline(sgqlc.types.Type, AlertableEntityOutline, EntityOutline):
    __schema__ = nerdgraph
    __field_names__ = ("created_at", "created_by_user", "updated_at", "workload_status")
    created_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="createdAt")

    created_by_user = sgqlc.types.Field(UserReference, graphql_name="createdByUser")

    updated_at = sgqlc.types.Field(EpochMilliseconds, graphql_name="updatedAt")

    workload_status = sgqlc.types.Field(WorkloadStatus, graphql_name="workloadStatus")


class WorkloadRollupRuleStatusResult(sgqlc.types.Type, WorkloadStatusResult):
    __schema__ = nerdgraph
    __field_names__ = ("rollup_rule_details",)
    rollup_rule_details = sgqlc.types.Field(
        WorkloadRollupRuleDetails, graphql_name="rollupRuleDetails"
    )


class WorkloadStaticStatusResult(sgqlc.types.Type, WorkloadStatusResult):
    __schema__ = nerdgraph
    __field_names__ = ("description", "summary")
    description = sgqlc.types.Field(String, graphql_name="description")

    summary = sgqlc.types.Field(String, graphql_name="summary")


class AiNotificationsAuth(sgqlc.types.Union):
    __schema__ = nerdgraph
    __types__ = (
        AiNotificationsBasicAuth,
        AiNotificationsOAuth2Auth,
        AiNotificationsTokenAuth,
    )


class AiNotificationsError(sgqlc.types.Union):
    __schema__ = nerdgraph
    __types__ = (
        AiNotificationsConstraintsError,
        AiNotificationsDataValidationError,
        AiNotificationsResponseError,
        AiNotificationsSuggestionError,
    )


class AiWorkflowsConfiguration(sgqlc.types.Union):
    __schema__ = nerdgraph
    __types__ = (AiWorkflowsNrqlConfiguration,)


class AlertsNotificationChannelMutation(sgqlc.types.Union):
    __schema__ = nerdgraph
    __types__ = (
        AlertsEmailNotificationChannel,
        AlertsOpsGenieNotificationChannel,
        AlertsPagerDutyNotificationChannel,
        AlertsSlackNotificationChannel,
        AlertsVictorOpsNotificationChannel,
        AlertsWebhookNotificationChannel,
        AlertsXMattersNotificationChannel,
    )


class IncidentIntelligenceEnvironmentCreateEnvironmentResultDetails(sgqlc.types.Union):
    __schema__ = nerdgraph
    __types__ = (
        IncidentIntelligenceEnvironmentEnvironmentAlreadyExists,
        IncidentIntelligenceEnvironmentEnvironmentCreated,
    )


class IncidentIntelligenceEnvironmentCurrentEnvironmentResultReasonDetails(
    sgqlc.types.Union
):
    __schema__ = nerdgraph
    __types__ = (
        IncidentIntelligenceEnvironmentMultipleEnvironmentsAvailable,
        IncidentIntelligenceEnvironmentUserNotAuthorizedForAccount,
        IncidentIntelligenceEnvironmentUserNotCapableToOperateOnAccount,
    )


class Nr1CatalogDataSourceInstallDirective(sgqlc.types.Union):
    __schema__ = nerdgraph
    __types__ = (Nr1CatalogLinkInstallDirective, Nr1CatalogNerdletInstallDirective)


class Nr1CatalogSearchResult(sgqlc.types.Union):
    __schema__ = nerdgraph
    __types__ = (
        Nr1CatalogAlertPolicyTemplate,
        Nr1CatalogDashboardTemplate,
        Nr1CatalogDataSource,
        Nr1CatalogNerdpack,
        Nr1CatalogQuickstart,
    )
